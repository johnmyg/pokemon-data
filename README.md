# 🧾 Pokémon TCG eBay Sales Scraper

A data pipeline for scraping and analyzing eBay sold listings of Pokémon TCG cards. This project helps collect structured data on individual card sales, including grading details, pricing, and set information — enabling analysis of trends, price ranges, and market behavior.

## 📦 Features

-   Scrapes sold listings for Pokémon TCG cards from eBay
-   Extracts raw listing info including title, price, condition, sale date, etc...
-   Parses grading company (PSA, BGS, CGC, etc.) and grade
-   Filters out unwanted listings (e.g., lots, proxies, bundles)
-   Outputs clean, structured CSV

## Raw Data Model

| Field Name       | Description |
|------------------|-----------------------------------------|
| `id`             | Unique listing ID (hash or UUID)        |
| `title`          | Raw listing title from eBay             |
| `sold_price`     | Final sale price (excluding shipping)   |
| `sold_date`      | Date of sale                            |
| `shipping_cost`  | Shipping cost (if available)            |
| `total_price`    | Sum of `sold_price` + `shipping_cost`   |
| `listing_url`    | Link to the original eBay listing       |

## Cleaned Data Model

- Clean and Add the following
| Field Name       | Description |
| `raw_or_graded`  | Either `raw` or `graded`                |
| `grading_company`| PSA, BGS, CGC, etc. (`N/A` if raw)      |
| `grade`          | Card grade (e.g., "10", "9.5") or `N/A` |
| `set_name`       | Pokémon set                             |
| `is_lot`         | `true` if listing is a lot or bulk sale |
| `is_sealed`      | Link to the original eBay listing       |
