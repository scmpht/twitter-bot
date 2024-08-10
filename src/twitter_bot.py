import pandas as pd
import requests
from datetime import datetime, timedelta
from scrape_arxiv import scrape_arxiv
from tweet import tweet


def main(last_search, end_date):

    ### Define searches
    # lists = OR, tuples = AND
    # Each dictionary is a seperate search
    searches = [
        {
            "Title": [],
            "Abstract": [("machine learning", "omics")]
        },
        {
            "Title": ["glioblastoma", "glioma"],
            "Abstract": ["omics", ("therapy", "resist")]
        }
    ]

    # Scrape papers from bioRxiv
    relevant_papers = scrape_arxiv(searches, last_search, end_date)

    # Tweet the title and DOI
    if relevant_papers.shape[0] > 0:
        for _, paper in relevant_papers.iterrows():
            tweet(f"{paper['title']}: https://doi.org/{paper['doi']}")
    else:
        print("No new papers.")

    # Save scraped_papers
    past_papers = pd.read_csv("data/scraped_papers.csv")
    past_papers = pd.concat([relevant_papers, past_papers])
    past_papers = past_papers[~past_papers.duplicated()]
    past_papers.to_csv("data/scraped_papers.csv", index=False)
    
if __name__ == "__main__":
    main(
        last_search = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d'),
        end_date = datetime.today().strftime('%Y-%m-%d')
    )

