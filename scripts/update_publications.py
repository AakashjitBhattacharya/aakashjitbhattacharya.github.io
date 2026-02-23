import requests
import json
import time

ORCID_ID = "0000-0003-2188-6245"
ORCID_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

HEADERS = {
    "Accept": "application/json"
}

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"


def map_type(orcid_type):
    mapping = {
        "journal-article": "Journal",
        "conference-paper": "Conference",
        "book-chapter": "Book Chapter",
        "patent": "Patent"
    }
    return mapping.get(orcid_type, "Conference")


def get_citation_count(title):
    try:
        params = {
            "query": title,
            "fields": "citationCount",
            "limit": 1
        }

        response = requests.get(SEMANTIC_SCHOLAR_API, params=params)
        data = response.json()

        if data.get("data"):
            return data["data"][0].get("citationCount", 0)

        return 0

    except Exception:
        return 0


def get_publications():
    response = requests.get(ORCID_URL, headers=HEADERS)
    data = response.json()

    publications = []

    for group in data.get("group", []):
        work = group.get("work-summary", [])[0]

        title = work.get("title", {}).get("title", {}).get("value", "No Title")
        year = work.get("publication-date", {}).get("year", {}).get("value", "0")
        work_type = work.get("type", "conference-paper")
        pub_type = map_type(work_type)

        external_ids = work.get("external-ids", {}).get("external-id", [])
        link = "#"

        for ext in external_ids:
            if ext.get("external-id-url"):
                link = ext["external-id-url"]["value"]
                break

        print(f"Fetching citations for: {title}")
        citations = get_citation_count(title)
        time.sleep(1)  # Avoid API rate limit

        publication = {
            "title": title,
            "authors": "Aakashjit Bhattacharya et al.",
            "venue": work.get("journal-title", {}).get("value", "N/A"),
            "year": int(year) if year != "0" else 0,
            "type": pub_type,
            "citations": citations,
            "link": link
        }

        publications.append(publication)

    return publications


if __name__ == "__main__":
    pubs = get_publications()

    output = {
        "publications": pubs
    }

    with open("data/publications.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("Publications with citations updated successfully.")
