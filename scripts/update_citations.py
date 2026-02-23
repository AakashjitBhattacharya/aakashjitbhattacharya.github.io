# update_citations.py
# GitHub Action runner script that uses `scholarly` to fetch google scholar profile and write data/citations.json
# Requires: scholarly, requests
import json
from scholarly import scholarly
import datetime

GSCHOLAR_USER = "BLMncXIAAAAJ"  # from search results; change if needed

def fetch_profile(user_id):
    query = scholarly.search_author_id(user_id)
    author = scholarly.fill(query, sections=['basics','publications','indices'])
    return author

def main():
    author = fetch_profile(GSCHOLAR_USER)
    total_cites = author.get('citedby', 0) or author.get('indices', {}).get('citedby', 0)
    pubs = []
    for p in author.get('publications', [])[:200]:
        pub = {
            'title': p.get('bib', {}).get('title'),
            'year': p.get('bib', {}).get('pub_year'),
            'venue': p.get('bib', {}).get('venue'),
            'citations': p.get('num_citations', 0),
            'link': p.get('pub_url') or p.get('bib', {}).get('url')
        }
        pubs.append(pub)
    out = {
        'generated_at': datetime.datetime.utcnow().isoformat()+'Z',
        'total_citations': total_cites,
        'publications': pubs
    }
    with open('data/citations.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

if __name__ == '__main__':
    main()
