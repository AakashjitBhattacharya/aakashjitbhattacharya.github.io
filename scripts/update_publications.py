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
    if not orcid_type:
        return "Conference"

    orcid_type = orcid_type.lower()

    if "journal" in orcid_type:
        return "Journal"

    if "conference" in orcid_type:
        return "Conference"

    if "book" in orcid_type or "chapter" in orcid_type or "section" in orcid_type:
        return "Book Chapter"

    if "patent" in orcid_type:
        return "Patent"

    # Default fallback
    return "Conference"


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
        pub_date = work.get("publication-date")
        # Safe year extraction
        year = 0
        pub_date = work.get("publication-date")

        if pub_date:
            year_obj = pub_date.get("year")
            if year_obj and year_obj.get("value"):
            try:
                year = int(year_obj.get("value"))
            except:
                year = 0
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

        journal_title = work.get("journal-title")
        venue = journal_title.get("value") if journal_title else "N/A"

        publication = {
        "title": title,
        "authors": "Aakashjit Bhattacharya et al.",
        "venue": venue,
        "year": year,
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
