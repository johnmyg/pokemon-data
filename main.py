from src.scraper import fetch_ebay_search_results
from src.data_to_csv import write_to_csv
from src.utils import load_links


def main():
    links = load_links()

    all_data = []
    for link in links:
        results = fetch_ebay_search_results(link)
        all_data.extend(results)
    unique_data = {entry["id"]: entry for entry in all_data}.values()
    write_to_csv(list(unique_data))


if __name__ == "__main__":
    main()
