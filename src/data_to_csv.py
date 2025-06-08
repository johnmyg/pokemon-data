import csv
import os
from typing import List, Dict


def write_to_csv(data: List[Dict], filename: str, append: bool):
    if not data:
        print("No data to write.")
        return

    base_dir = os.path.dirname(os.path.dirname(__file__))
    target_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(target_dir, exist_ok=True)
    filepath = os.path.join(target_dir, filename)

    fieldnames = data[0].keys()
    mode = "a" if append else "w"
    write_header = not append or not os.path.exists(
        filepath
    )  # write header if not appending or file doesn't exist

    try:
        with open(filepath, mode=mode, newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerows(data)
        print(f"Data {'appended to' if append else 'written to'} {filepath}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")
