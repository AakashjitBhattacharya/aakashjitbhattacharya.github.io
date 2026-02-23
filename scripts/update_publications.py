import requests
import json
import time
import re

ORCID_ID = "0000-0003-2188-6245"
BASE_URL = "https://pub.orcid.org/v3.0"
HEADERS = {
    "Accept": "application/vnd.orcid+json"
}

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"


def clean_html(text):
    if not text:
        return ""
    return re.sub(r"<.*?>", "", text)


def classify_work(work):
    """
    Generic classification based on:
    - ORCID work type
    - container title
    - journal title presence
    """

    work_type = (work.get("type") or "").lower()

    # Direct mapping
    if "patent" in work_type:
        return "Patent"

    if "book-chapter" in work_type or "book-section" in work_type:
        return "Book Chapter"

    if "conference" in work_type:
        return "Conference"

    if "journal" in work_type:
        return "Journal"

    # Secondary logic based on container title
    journal_title = work.get("journal-title")
    if journal_title and journal_title.get("value"):
        return "Journal"

    # Fallback
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
    except:
        return 0


def get_full_work(put_code):
    url = f"{BASE_URL}/{ORCID_ID}/work/{put_code}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None


def get_publications():
    summary_url = f"{BASE_URL}/{ORCID_ID}/works"
    response = requests.get(summary_url, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch ORCID works")
        return []

    data = response.json()
    groups = data.get("group", [])

    publications = []

    for group in groups:
        summaries = group.get("work-summary", [])
        if not summaries:
            continue

        summary = summaries[0]
        put_code = summary.get("put-code")

        full_work = get_full_work(put_code)
        if not full_work:
            continue

        # -------- TITLE --------
        title = ""
        if full_work.get("title") and full_work["title"].get("title"):
            title = full_work["title"]["title"].get("value", "")
        title = clean_html(title)

        # -------- YEAR --------
        year = 0
        pub_date = full_work.get("publication-date")
        if pub_date and pub_date.get("year") and pub_date["year"].get("value"):
            try:
                year = int(pub_date["year"]["value"])
            except:
                year = 0

        # -------- VENUE --------
        venue = "N/A"
        journal_title = full_work.get("journal-title")
        if journal_title and journal_title.get("value"):
            venue = journal_title.get("value")

        # -------- LINK --------
        link = "#"
        external_ids = full_work.get("external-ids", {}).get("external-id", [])
        for ext in external_ids:
            if ext.get("external-id-url") and ext["external-id-url"].get("value"):
                link = ext["external-id-url"]["value"]
                break

        # -------- CLASSIFICATION --------
        pub_type = classify_work(full_work)

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
