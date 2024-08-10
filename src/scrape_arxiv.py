import pandas as pd
import requests
from datetime import datetime, timedelta


def search_bioarxiv(server, start_date, end_date, cursor=0):
    
    interval = f"{start_date}/{end_date}"
    
    response = requests.get(f"https://api.biorxiv.org/details/{server}/{interval}/{cursor}/json")
    if response.status_code == 200:
        
        result = response.json()
        papers = result['collection']

        if result['messages'][0]['count'] == 100:
            cursor += 100
            papers = papers + search_bioarxiv(server, start_date, end_date, cursor=cursor)
        
        return papers
    
    
    else:
        print(f"Error: {response.status_code}")
        return None
    
    
def scrape_arxiv(searches, last_search, end_date):
    past_papers = pd.read_csv("../data/scraped_papers.csv")
    scraped_papers = pd.DataFrame(search_bioarxiv('biorxiv', last_search, end_date))
    relevant_papers = scraped_papers.iloc[:0]

    for criteria in searches:
        
        filtered_papers = scraped_papers

        # Filter title criteria
        if len(criteria['Title']) > 0:
            filtered_papers = filtered_papers[
                filtered_papers['title'].apply(lambda x: 
                    any(all(subterm in x.lower() for subterm in term) if isinstance(term, tuple) else term in x.lower() for term in criteria['Title']))].copy()

        # Filter abstract criteria
        if len(criteria['Abstract']) > 0:
            filtered_papers = filtered_papers[
                filtered_papers['abstract'].apply(lambda x: 
                    any(all(subterm in x.lower() for subterm in term) if isinstance(term, tuple) else term in x.lower() for term in criteria['Abstract']))].copy()

        relevant_papers = pd.concat([relevant_papers, filtered_papers])

    relevant_papers = relevant_papers[~relevant_papers['doi'].isin(past_papers['doi'])]
    
    return relevant_papers
        