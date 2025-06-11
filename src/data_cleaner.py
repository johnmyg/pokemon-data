import pandas as pd
import re
from pokemon_names import pokemon_names, set_names
from datetime import datetime


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)


def clean_pokemon_data(
    input_file="./data/raw/ebay_listings_2025-06-07.csv", output_file=None
):

    # Read csv file
    df = pd.read_csv(input_file)

    print(f"CSV file rows: {len(df)}")

    # Create a copy for cleaning
    cleaned_df = df.copy()

    # 1. Remove MTG/Magic the Gathering cards
    mtg_pattern = r"(?i)(mtg|magic.*gathering|magic:.*gathering)"
    cleaned_df = cleaned_df[~cleaned_df["title"].str.contains(mtg_pattern, na=False)]
    print(f"After removing MTG cards: {len(cleaned_df)} rows")

    # 2. Remove lot/bulk listings
    lot_pattern = r"(?i)(lot|bulk)"
    cleaned_df = cleaned_df[~cleaned_df["title"].str.contains(lot_pattern, na=False)]
    print(f"After removing lot/bulk listings: {len(cleaned_df)} rows")

    # 3. Remove code cards/coins
    code_pattern = r"(?i)(code.*card|tcg.*code|online.*code|coin|token)"
    cleaned_df = cleaned_df[~cleaned_df["title"].str.contains(code_pattern, na=False)]
    print(f"After removing code cards/coins: {len(cleaned_df)} rows")

    # 4. Remove other languages (Korean, Japanese)
    lang_pattern = r"(?i)(korean|japanese|日本語|한국어|jpn|kor)"
    cleaned_df = cleaned_df[~cleaned_df["title"].str.contains(lang_pattern, na=False)]
    print(f"After removing other languages: {len(cleaned_df)} rows")

    cleaned_df["product_type"] = cleaned_df["title"].apply(determine_product_type)

    cleaned_df = cleaned_df.reset_index(drop=True)

    return cleaned_df.head()


def determine_product_type(title):
    """Determine if product is raw, graded, or sealed based on title"""

    # Check for sealed products first
    sealed_keywords = [
        "booster",
        "pack",
        "box",
        "case",
        "sealed",
        "factory sealed",
        "blaster",
        "hobby box",
        "retail box",
        "jumbo pack",
        "fat pack",
        "theme deck",
        "starter deck",
        "bundle",
        "collection box",
        "tin",
        "etb",
        "elite trainer box",
        "premium collection",
    ]

    title_lower = title.lower()

    for keyword in sealed_keywords:
        if keyword in title_lower:
            return "sealed"

    # Check for grading companies
    grading_companies = ["psa", "bgs", "cgc", "beckett", "sgc"]

    for company in grading_companies:
        if company in title_lower:
            return "graded"

    # Look for grade patterns like "PSA 10", "BGS 9.5"
    grade_pattern = r"(?i)(psa|bgs|cgc|beckett|sgc)\s*\d+(\.\d+)?"
    if re.search(grade_pattern, title):
        return "graded"

    # If not sealed or graded, it's raw
    return "raw"


if __name__ == "__main__":
    print(clean_pokemon_data())
