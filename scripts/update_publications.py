import requests
import json
import time

ORCID_ID = "0000-0003-2188-6245"
ORCID_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

HEADERS = {
    "Accept": "application/vnd.orcid+json"
}

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"


def map_type(orcid_type):
    if not orcid_type:
        return "Conference"

    t = orcid_type.lower()

    # JOURNAL
    if "journal" in t or "article" in t:
        return "Journal"

    # CONFERENCE
    if "conference" in t or "proceeding" in t:
        return "Conference"

    # BOOK CHAPTER
    if "book" in t or "chapter" in t or "section" in t:
        return "Book Chapter"

    # PATENT
    if "patent" in t:
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

    if response.status_code != 200:
        print("Failed to fetch ORCID data")
        return []

    data = response.json()
    groups = data.get("group", [])

    publications = []

    for group in groups:
        summaries = group.get("work-summary", [])
        if not summaries:
            continue

        work = summaries[0]

        # -------- TITLE --------
        title = "No Title"
        if work.get("title") and work["title"].get("title"):
            title = work["title"]["title"].get("value", "No Title")

        # -------- TYPE --------
        work_type = work.get("type", "")
        pub_type = map_type(work_type)

        # -------- YEAR --------
        year = 0
        pub_date = work.get("publication-date")
        if pub_date:
            year_obj = pub_date.get("year")
            if year_obj and year_obj.get("value"):
                try:
                    year = int(year_obj.get("value"))
                except:
                    year = 0

        # -------- VENUE --------
        venue = "N/A"
        journal_title = work.get("journal-title")
        if journal_title and journal_title.get("value"):
            venue = journal_title.get("value")

        # -------- LINK --------
        link = "#"
        external_ids = work.get("external-ids", {}).get("external-id", [])
        for ext in external_ids:
            if ext.get("external-id-url") and ext["external-id-url"].get("value"):
                link = ext["external-id-url"]["value"]
                break

        # -------- CITATIONS --------
        print(f"Fetching citations for: {title}")
        citations = get_citation_count(title)
        time.sleep(1)

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

    print("Publications updated successfully.")
