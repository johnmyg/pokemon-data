import csv
import os
from typing import List, Dict


def write_to_csv(data: List[Dict], filename: str = "ebay_listings.csv"):
    if not data:
        print("No data to write.")
        return

    # Get full path to ../data/raw/ebay_listings.csv
    base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from /src
    target_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(target_dir, exist_ok=True)  # Create the directory if it doesn't exist
    filepath = os.path.join(target_dir, filename)

    # Extract fieldnames from the first dictionary
    fieldnames = data[0].keys()

    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully written to {filepath}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")
