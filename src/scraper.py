import requests
from bs4 import BeautifulSoup


def fetch_ebay_search_results(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # On Ebay Each listing is of type <li> with class <s-item>
    # This will find all the listings on the page
    listings = soup.find_all("li", class_="s-item")

    print(f"Found {len(listings)} listings")
