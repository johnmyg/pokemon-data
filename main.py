from src.scraper import fetch_ebay_search_results
from src.data_to_csv import write_to_csv
from src.utils import load_links
from datetime import datetime, timedelta
import sys


def main(daily_mode=False):

    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime("%b %-d, %Y")
    filename = f"ebay_listings_{formatted_date}.csv"  # filename with date

    links = load_links()

    all_data = []
    for link in links:
        results = fetch_ebay_search_results(link, daily_mode, formatted_date)
        all_data.extend(results)
    unique_data = {entry["id"]: entry for entry in all_data}.values()

    if daily_mode:
        write_to_csv(list(unique_data), filename, append=True)
    else:
        write_to_csv(list(unique_data), "ebay_listings.csv")


if __name__ == "__main__":
    daily_mode = "--daily" in sys.argv
    main(daily_mode)
