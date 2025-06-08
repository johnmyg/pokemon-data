import requests
import re
from bs4 import BeautifulSoup, Tag
import json

# pyright: reportGeneralTypeIssues=false


def fetch_ebay_search_results(start_url, daily: bool, yesterday):

    headers = {"User-Agent": "Mozilla/5.0"}
    url = start_url
    data = []
    visited_urls = set()
    page_count = 1
    # Ebay stops showing data over page 200
    # 10 is set for daily
    # we link would have more than 2400 sold listings in a day
    MAX_PAGES = 10 if daily else 200

    while url and url not in visited_urls and page_count < MAX_PAGES:
        visited_urls.add(url)
        page_count += 1

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        # All sold listings on ebay are wrapped inside this ul
        container = soup.find("ul", class_="srp-results srp-list clearfix")
        if container is None:
            print("Could not find listings container.")
            return []

        # On Ebay Each listing is of type <li> with class <s-item>
        # This will find all the listings inside the container
        listings = container.find_all("li", class_="s-item")

        for item in listings:

            # Listing URL and ID
            link_tag = item.find("a", class_="s-item__link")
            listing_url = link_tag["href"] if link_tag else ""

            listing_id = ""
            # use regex to find id off link
            # which is located after /itm/
            if listing_url:
                match = re.search(r"/itm/(\d+)", listing_url)
                if match:
                    listing_id = match.group(1)

            # Title
            title_div = (
                link_tag.find("div", class_="s-item__title") if link_tag else None
            )
            title = title_div.get_text(strip=True) if title_div else ""

            # Sold date
            sold_date_span = item.find(
                "span", class_="s-item__caption--signal POSITIVE"
            )
            sold_date = (
                sold_date_span.get_text(strip=True).replace("Sold", "").strip()
                if sold_date_span
                else ""
            )

            # Sold price
            price_span = item.find("span", class_="s-item__price")
            sold_price = 0.0
            if price_span:
                # Extract number from price text, e.g. "$200.00"
                price_text = price_span.get_text(strip=True)
                price_match = re.search(r"\$([\d,\.]+)", price_text)
                if price_match:
                    sold_price = float(price_match.group(1).replace(",", ""))

            # Shipping cost
            shipping_span = item.find("span", class_="s-item__shipping")
            shipping_cost = 0.0
            if shipping_span:
                shipping_text = shipping_span.get_text(strip=True)
                if "Free" in shipping_text:
                    shipping_cost = 0.0
                else:
                    ship_match = re.search(r"\$([\d,\.]+)", shipping_text)
                    if ship_match:
                        shipping_cost = float(ship_match.group(1).replace(",", ""))

            total_price = sold_price + shipping_cost

            # check if daily is true and sold_date equals yesterday
            # if so append the listing to data

            if daily and sold_date != yesterday:
                continue  # Skip if it's not from yesterday

            data.append(
                {
                    "id": listing_id,
                    "title": title,
                    "sold_date": sold_date,
                    "sold_price": sold_price,
                    "shipping_cost": shipping_cost,
                    "total_price": total_price,
                    "listing_url": listing_url,
                }
            )

        # Logic to find next page
        next_page_tag = soup.find("a", class_="pagination__next")
        print(next_page_tag)
        url = next_page_tag.get("href") if next_page_tag else None

    return data
