import pandas as pd
import re
from datetime import datetime


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

    print(df.head())


if __name__ == "__main__":
    clean_pokemon_data()
