from src.scraper import fetch_ebay_search_results
from src.data_to_csv import write_to_csv
from src.utils import load_links, get_yesterday_dates, upload_file_to_s3
import sys
import os


def main(daily_mode=False):

    formatted_date, filename_date = get_yesterday_dates()
    filename = f"ebay_listings_{filename_date}.csv"
    object_name = f"data/raw/{filename}"
    file_path = os.path.join("data", "raw", filename)

    links = load_links()

    all_data = []
    for link in links:
        results = fetch_ebay_search_results(link, daily_mode, formatted_date)
        all_data.extend(results)
    unique_data = {entry["id"]: entry for entry in all_data}.values()

    if daily_mode:
        write_to_csv(list(unique_data), filename, append=True)
        upload_file_to_s3(file_path, file_path)
    else:
        write_to_csv(list(unique_data), "ebay_listings.csv", False)


if __name__ == "__main__":
    daily_mode = "--daily" in sys.argv
    main(daily_mode)
