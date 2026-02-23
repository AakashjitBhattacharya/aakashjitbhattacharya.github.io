import requests
import json
import datetime

ORCID_ID = "0000-0003-2188-6245"

def fetch_orcid_works(orcid):
    url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def main():
    data = fetch_orcid_works(ORCID_ID)
    works = data.get("group", [])
    publications = []

    for work in works:
        summary = work["work-summary"][0]
        title = summary["title"]["title"]["value"]
        year = summary.get("publication-date", {}).get("year", {}).get("value", "")
        publications.append({
            "title": title,
            "year": year,
            "citations": 0  # Scholar citation not available via API
        })

    output = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_citations": "Update from Google Scholar manually",
        "publications": publications
    }

    with open("data/citations.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
