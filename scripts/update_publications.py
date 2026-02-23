import requests
import json
import time
import re

ORCID_ID = "0000-0003-2188-6245"
BASE_URL = "https://pub.orcid.org/v3.0"
HEADERS = {"Accept": "application/vnd.orcid+json"}

CROSSREF_API = "https://api.crossref.org/works/"
SEMANTIC_API = "https://api.semanticscholar.org/graph/v1/paper/DOI:"

MY_NAME_KEYWORDS = ["aakashjit", "bhattacharya"]


# ---------------- CLEAN HTML ----------------
def clean_html(text):
    if not text:
        return ""
    return re.sub(r"<.*?>", "", text)


# ---------------- CROSSREF CLASSIFICATION ----------------
def classify_via_crossref(doi):
    try:
        r = requests.get(CROSSREF_API + doi)
        if r.status_code != 200:
            return None

        work_type = r.json()["message"].get("type", "").lower()

        if "posted-content" in work_type:
            return "Preprint"
        if "journal-article" in work_type:
            return "Journal"
        if "proceedings-article" in work_type:
            return "Conference"
        if "book-chapter" in work_type:
            return "Book Chapter"
        if "book" in work_type:
            return "Book Chapter"
        if "patent" in work_type:
            return "Patent"

        return None
    except:
        return None


# ---------------- FALLBACK CLASSIFICATION ----------------
def classify_fallback(work):
    work_type = (work.get("type") or "").lower()

    if "preprint" in work_type:
        return "Preprint"
    if "patent" in work_type:
        return "Patent"
    if "book" in work_type:
        return "Book Chapter"
    if "conference" in work_type:
        return "Conference"
    if "journal" in work_type:
        return "Journal"

    journal_title = work.get("journal-title")
    if journal_title and journal_title.get("value"):
        venue = journal_title.get("value").lower()
        if "arxiv" in venue or "ssrn" in venue or "techrxiv" in venue:
            return "Preprint"
        return "Journal"

    return "Conference"


# ---------------- CITATIONS VIA DOI ----------------
def get_citation_count(doi):
    if not doi:
        return 0

    try:
        r = requests.get(
            SEMANTIC_API + doi,
            params={"fields": "citationCount"}
        )
        if r.status_code != 200:
            return 0

        return r.json().get("citationCount", 0)
    except:
        return 0


# ---------------- FETCH FULL WORK ----------------
def get_full_work(put_code):
    url = f"{BASE_URL}/{ORCID_ID}/work/{put_code}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return None


# ---------------- MAIN LOGIC ----------------
def get_publications():

    summary_url = f"{BASE_URL}/{ORCID_ID}/works"
    r = requests.get(summary_url, headers=HEADERS)

    if r.status_code != 200:
        print("Failed to fetch ORCID works")
        return []

    groups = r.json().get("group", [])
    publications = []

    for group in groups:

        summaries = group.get("work-summary", [])
        if not summaries:
            continue

        put_code = summaries[0].get("put-code")
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
        ext_ids = full_work.get("external-ids", {}).get("external-id", [])
        for ext in ext_ids:
            if ext.get("external-id-type", "").lower() == "doi":
                doi = ext.get("external-id-value")
                break

        # -------- CLASSIFICATION --------
        pub_type = None
        if doi:
            pub_type = classify_via_crossref(doi)

        if not pub_type:
            pub_type = classify_fallback(full_work)

        # -------- AUTHORS --------
        authors_list = []
        is_first_author = False

        contributors = full_work.get("contributors", {}).get("contributor", [])

        for idx, contributor in enumerate(contributors):
            credit_name = contributor.get("credit-name")
            if credit_name and credit_name.get("value"):
                name = credit_name["value"]
                authors_list.append(name)

                if idx == 0:
                    name_lower = name.lower()
                    if all(k in name_lower for k in MY_NAME_KEYWORDS):
                        is_first_author = True

        authors = ", ".join(authors_list) if authors_list else "N/A"

        # -------- VENUE --------
        venue = "N/A"
        journal_title = full_work.get("journal-title")
        if journal_title and journal_title.get("value"):
            venue = journal_title.get("value")

        # -------- CITATIONS --------
        citations = get_citation_count(doi)
        time.sleep(1)

        publication = {
            "title": title,
            "authors": authors,
            "venue": venue,
            "year": year,
            "type": pub_type,
            "citations": citations,
            "link": f"https://doi.org/{doi}" if doi else "#",
            "is_first_author": is_first_author
        }

        publications.append(publication)

    return publications


if __name__ == "__main__":

    pubs = get_publications()

    with open("data/publications.json", "w", encoding="utf-8") as f:
        json.dump({"publications": pubs}, f, indent=4)

    print("Publications updated successfully.")
