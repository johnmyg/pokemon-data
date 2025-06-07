from src.scraper import fetch_ebay_search_results


def main():
    fetch_ebay_search_results(
        "https://www.ebay.com/sch/i.html?_nkw=Pokemon+Journey+Together&_sacat=0&_from=R40&LH_Sold=1&LH_Complete=1&_ipg=240&_pgn=1&rt=nc"
    )


if __name__ == "__main__":
    main()
