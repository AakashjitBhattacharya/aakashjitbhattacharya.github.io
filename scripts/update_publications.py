import requests
import json
import time
import re

ORCID_ID = "0000-0003-2188-6245"
BASE_URL = "https://pub.orcid.org/v3.0"
HEADERS = {"Accept": "application/vnd.orcid+json"}

CROSSREF_API = "https://api.crossref.org/works/"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"


# ---------------- CLEAN HTML ----------------
def clean_html(text):
    if not text:
        return ""
    return re.sub(r"<.*?>", "", text)


# ---------------- CROSSREF CLASSIFICATION ----------------
def classify_via_crossref(doi):
    try:
        response = requests.get(CROSSREF_API + doi)
        if response.status_code != 200:
            return None

        data = response.json()
        work_type = data["message"].get("type", "").lower()

        # -------- PREPRINT --------
        if "posted-content" in work_type:
            return "Preprint"

        # -------- JOURNAL --------
        if "journal-article" in work_type:
            return "Journal"

        # -------- CONFERENCE --------
        if "proceedings-article" in work_type:
            return "Conference"

        # -------- BOOK CHAPTER --------
        if "book-chapter" in work_type:
            return "Book Chapter"

        if "book" in work_type:
            return "Book Chapter"

        # -------- PATENT --------
        if "patent" in work_type:
            return "Patent"

        return None
    except:
        return None


# ---------------- FALLBACK CLASSIFICATION ----------------
def classify_fallback(work):
    work_type = (work.get("type") or "").lower()

    # -------- PREPRINT --------
    if "preprint" in work_type:
        return "Preprint"

    # -------- PATENT --------
    if "patent" in work_type:
        return "Patent"

    # -------- BOOK --------
    if "book" in work_type:
        return "Book Chapter"

    # -------- CONFERENCE --------
    if "conference" in work_type:
        return "Conference"

    # -------- JOURNAL --------
    if "journal" in work_type:
        return "Journal"

    # -------- Check journal-title for arXiv etc --------
    journal_title = work.get("journal-title")
    if journal_title and journal_title.get("value"):
        venue_name = journal_title.get("value").lower()

        if "arxiv" in venue_name or "ssrn" in venue_name or "techrxiv" in venue_name:
            return "Preprint"

        return "Journal"

    return "Conference"

# ---------------- CITATIONS ----------------
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


# ---------------- GET FULL WORK ----------------
def get_full_work(put_code):
    url = f"{BASE_URL}/{ORCID_ID}/work/{put_code}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None


# ---------------- MAIN FUNCTION ----------------
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

        # -------- DOI --------
        doi = None
        external_ids = full_work.get("external-ids", {}).get("external-id", [])
        for ext in external_ids:
            if ext.get("external-id-type", "").lower() == "doi":
                doi = ext.get("external-id-value")
                break

        # -------- CLASSIFICATION --------
        pub_type = None
        if doi:
            pub_type = classify_via_crossref(doi)

        if not pub_type:
            pub_type = classify_fallback(full_work)

        # -------- VENUE --------
        venue = "N/A"
        journal_title = full_work.get("journal-title")
        if journal_title and journal_title.get("value"):
            venue = journal_title.get("value")

        # -------- LINK --------
        link = f"https://doi.org/{doi}" if doi else "#"

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
