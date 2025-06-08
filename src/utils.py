def load_links(filepath: str = "data/links.txt") -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]
    return links
