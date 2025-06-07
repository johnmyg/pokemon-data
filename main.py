from src.scraper import fetch_ebay_search_results
from src.data_to_csv import write_to_csv


def main():
    data = fetch_ebay_search_results(
        "https://www.ebay.com/sch/i.html?_nkw=Pokemon+Journey+Together&_sacat=0&_from=R40&LH_Sold=1&LH_Complete=1&_ipg=240&_pgn=1&rt=nc"
    )
    write_to_csv(data)


if __name__ == "__main__":
    main()
