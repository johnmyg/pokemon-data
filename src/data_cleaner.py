import pandas as pd
import re
from pokemon_names import pokemon_names, set_names
from datetime import datetime
from utils import upload_file_to_s3

# pyright: reportGeneralTypeIssues=false

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)


def clean_pokemon_data(
    input_file="./data/raw/ebay_listings_2025-06-07.csv", output_file=None
):

    # Read csv file
    df = pd.read_csv(input_file)

    # print(f"CSV file rows: {len(df)}")

    # Create a copy for cleaning
    cleaned_df = df.copy()

    # Remove MTG/Magic the Gathering cards
    mtg_pattern = r"(?i)(mtg|magic.*gathering|magic:.*gathering)"
    cleaned_df = cleaned_df[~cleaned_df["title"].str.contains(mtg_pattern, na=False)]
    # print(f"After removing MTG cards: {len(cleaned_df)} rows")

    # Remove lot/bulk listings/choose your card/oversized /jumbo/mystery/card database
    lot_pattern = r"(?i)(lot|bulk|choose|oversized|jumbo|mystery|database|sticker|binder|pick|custom|hot box)"
    cleaned_df = cleaned_df[~cleaned_df["title"].str.contains(lot_pattern, na=False)]
    # print(f"After removing lot/bulk listings: {len(cleaned_df)} rows")

    # Remove code cards/coins
    code_pattern = r"(?i)(code.*card|tcg.*code|online.*code|coin|token|codes)"
    cleaned_df = cleaned_df[~cleaned_df["title"].str.contains(code_pattern, na=False)]
    # print(f"After removing code cards/coins: {len(cleaned_df)} rows")

    # Remove other languages (Korean, Japanese)
    lang_pattern = r"(?i)(korean|japanese|japan|日本語|한국어|jpn|kor|chinese)"
    cleaned_df = cleaned_df[~cleaned_df["title"].str.contains(lang_pattern, na=False)]
    # print(f"After removing other languages: {len(cleaned_df)} rows")

    cleaned_df["product_type"] = cleaned_df["title"].apply(determine_product_type)
    cleaned_df["grading_company"] = cleaned_df["title"].apply(get_grading_company)
    cleaned_df["grade"] = cleaned_df["title"].apply(get_grade)
    cleaned_df = cleaned_df.reset_index(drop=True)
    cleaned_df["set_name"] = cleaned_df["title"].apply(get_set_name)
    cleaned_df["sealed_type"] = cleaned_df.apply(get_sealed_type, axis=1)

    return cleaned_df.head(50)


def determine_product_type(title):
    """Determine if product is raw, graded, or sealed based on title"""

    title_lower = title.lower()

    # some exceptions
    if "pack fresh" in title_lower:
        return "raw"

    # Check for sealed products first
    sealed_keywords = [
        "booster",
        "pack",
        "box",
        "case",
        "factory sealed",
        "blaster",
        "hobby box",
        "retail box",
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
        if re.search(rf"\b{re.escape(keyword)}\b", title_lower):
            return "sealed"

    # Check for grading companies
    if get_grading_company(title):
        return "graded"

    # Look for grade patterns like "PSA 10", "BGS 9.5"
    grade_pattern = r"(?i)(psa|bgs|cgc|beckett|sgc|vcg)\s*\d+(\.\d+)?"
    if re.search(grade_pattern, title):
        return "graded"

    # If not sealed or graded, it's raw
    return "raw"


def get_grading_company(title):
    title_lower = title.lower()

    # Check for grading companies
    grading_companies = {
        "psa": "PSA",
        "bgs": "BGS",
        "cgc": "CGC",
        "beckett": "BGS",
        "sgc": "SGC",
        "tag": "TAG",
        "vcg": "VCG",
    }

    for key, value in grading_companies.items():
        # 1. Match formats like "psa10", "beckett 9.5"
        grade_pattern = rf"{key}\s*\d+(\.\d+)?"
        if re.search(grade_pattern, title_lower):
            return value

        # 2. Just check if the grading company appears
        if re.search(rf"\b{key}\b", title_lower):
            return value


def get_grade(title):
    """Extract grade from title"""
    # Look for patterns like "PSA 10", "BGS 9.5", "CGC 8.5"
    title_lower = title.lower()

    # Special case for cgc pristine 10
    pristine_pattern = r"\bcgc\s*pristine\s*10\b"
    match = re.search(pristine_pattern, title_lower)
    if match:
        return "Pristine 10"

    grade_patterns = [
        r"(?i)(psa|bgs|cgc|beckett|sgc|tag|vcg)\s*(\d+(?:\.\d+)?)",
        r"(?i)grade\s*(\d+(?:\.\d+)?)",
        r"(?i)graded\s*(\d+(?:\.\d+)?)",
    ]

    for pattern in grade_patterns:
        match = re.search(pattern, title_lower)
        if match:
            # Return the grade number (last group in the match)
            return match.group(match.lastindex)

    return ""


def get_set_name(title):

    title_lower = title.lower()

    for key, value in set_names.items():
        # Use word boundaries to avoid partial matches,
        # but be careful with keys like "swsh1" which might not need word boundaries.

        # If key contains only letters and spaces, use word boundaries:
        if re.match(r"^[a-z\s&]+$", key):
            pattern = rf"\b{re.escape(key)}\b"
        else:
            # For keys with digits or special chars, just check if contained:
            pattern = re.escape(key)

        if re.search(pattern, title_lower):
            return value

    return ""


def get_sealed_type(row):
    title_lower = row["title"].lower()
    if row["product_type"] != "sealed":
        return ""
    keyword_map = {
        "booster box": "Booster Box",
        "booster pack": "Booster Pack",
        "elite trainer box": "Elite Trainer Box",
        "etb": "Elite Trainer Box",
        "theme deck": "Theme Deck",
        "starter deck": "Starter Deck",
        "collection box": "Collection Box",
        "blister pack": "Blister Pack",
        "fat pack": "Fat Pack",
        "hobby box": "Hobby Box",
        "retail box": "Retail Box",
        "tin": "Tin",
        "bundle": "Bundle",
        "case": "Case",
    }

    for keyword, label in keyword_map.items():
        # Escape the keyword for safe regex and add word boundaries
        pattern = rf"\b{re.escape(keyword)}\b"
        if re.search(pattern, title_lower, flags=re.IGNORECASE):
            return label

    return "Sealed Product"


if __name__ == "__main__":
    print(clean_pokemon_data())
