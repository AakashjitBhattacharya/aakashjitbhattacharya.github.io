
import requests
import json

ORCID_ID = 0000-0003-2188-6245
URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

headers = {
    "Accept": "application/json"
}

def map_type(orcid_type):
    mapping = {
        "journal-article": "Journal",
        "conference-paper": "Conference",
        "book-chapter": "Book Chapter",
        "patent": "Patent"
    }
    return mapping.get(orcid_type, "Conference")

def get_publications():
    response = requests.get(URL, headers=headers)
    data = response.json()

    publications = []

    for group in data.get("group", []):
        work = group.get("work-summary", [])[0]

        title = work.get("title", {}).get("title", {}).get("value", "No Title")
        year = work.get("publication-date", {}).get("year", {}).get("value", "N/A")
        work_type = work.get("type", "conference-paper")
        pub_type = map_type(work_type)

        external_ids = work.get("external-ids", {}).get("external-id", [])
        link = "#"

        for ext in external_ids:
            if ext.get("external-id-url"):
                link = ext["external-id-url"]["value"]
                break

        publication = {
            "title": title,
            "authors": "Aakashjit Bhattacharya et al.",
            "venue": work.get("journal-title", {}).get("value", "N/A"),
            "year": int(year) if year != "N/A" else 0,
            "type": pub_type,
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
