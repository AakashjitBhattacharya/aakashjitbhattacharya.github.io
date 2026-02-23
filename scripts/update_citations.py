# update_citations.py
# Only updates total citation count from Google Scholar
# Publications are maintained separately in publications.json

import json
import datetime
import requests
from bs4 import BeautifulSoup

GSCHOLAR_USER = "BLMncXIAAAAJ"
SCHOLAR_URL = f"https://scholar.google.com/citations?user={GSCHOLAR_USER}&hl=en"

def fetch_total_citations():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(SCHOLAR_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Scholar citation count is inside table with class gsc_rsb_st
    table = soup.find("table", {"id": "gsc_rsb_st"})

    if not table:
        return 0

    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if cols and "Citations" in cols[0].text:
            return int(cols[1].text.strip())

    return 0


def main():
    total_cites = fetch_total_citations()

    output = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_citations": total_cites
    }

    with open("data/citations.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()
