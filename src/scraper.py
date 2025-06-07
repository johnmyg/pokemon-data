import requests
import re
from bs4 import BeautifulSoup, Tag
import json


def fetch_ebay_search_results(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # All sold listings on ebay are wrapped inside this ul
    container = soup.find("ul", class_="srp-results srp-list clearfix")
    if container is None:
        print("Could not find listings container.")
        return []

    assert isinstance(
        container, Tag
    )  # that container is definitely a Tag, which removes the "no-member" warning when calling .find_all()

    # On Ebay Each listing is of type <li> with class <s-item>
    # This will find all the listings inside the container
    listings = container.find_all("li", class_="s-item")

    data = []
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
        title_div = link_tag.find("div", class_="s-item__title") if link_tag else None
        title = title_div.get_text(strip=True) if title_div else ""

        # Sold date
        sold_date_span = item.find("span", class_="s-item__caption--signal POSITIVE")
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

    print(json.dumps(data[0], indent=2))
