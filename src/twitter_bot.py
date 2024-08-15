import pandas as pd
import requests
from datetime import datetime, timedelta
from scrape_arxiv import scrape_arxiv
from tweet import tweet, shorten_url
from generate_summary import generate_summary, get_abstract, verify_tweet
from scrape_scholar import scholar_search, scrape_text


def main(last_search, end_date):

    ### BioRxiv
    # lists = OR, tuples = AND
    # Each dictionary is a seperate search
    biorxiv_searches = [
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
    relevant_papers = scrape_arxiv(biorxiv_searches, last_search, end_date)

    # Tweet a summary and DOI
    if relevant_papers.shape[0] > 0:
        for _, paper in relevant_papers.iterrows():
            summary = generate_summary(paper['abstract'])
            link = shorten_url(f"https://doi.org/{paper['doi']}")
            content = f"{summary} {link}"
            if len(content) <= 280:
                tweet(content)
            else:
                print(f"Size of tweet exceeded max: {len(content)}\n{paper['link']}\n{content}")

    else:
        print("No new bioRxiv papers.")

    # Save scraped_papers
    past_papers = pd.read_csv("data/scraped_papers.csv")
    past_papers = pd.concat([relevant_papers, past_papers])
    past_papers = past_papers[~past_papers.duplicated()]
    past_papers.to_csv("data/scraped_papers.csv", index=False)
    
    
    
    ### Google Scholar
    scholar_searches = [
    'omics AND machine learning',
    'allintitle: (glioblastoma OR glioma) AND (omics OR longitudinal OR "therapy resistance")'
    ]
    
    relevant_papers = scholar_search(scholar_searches)
    
    # Extract abstract, and tweet with link
    if relevant_papers.shape[0] > 0:
        for _, paper in relevant_papers.iterrows():
            
            if "proquest" in paper['link']:
                continue
            web_text = scrape_text(paper['link'])
        
            abstract = get_abstract(web_text)
            summary = generate_summary(abstract)
            
            if "**skip**" in summary:
                print("Couldn't identify abstract.")
                continue
            
            link = shorten_url(paper['link'])
            content = f"{summary} {link}"
            if len(content) <= 280:
                relevant = verify_tweet(paper['title'], content)
                if 'yes' in relevant.lower():
                    tweet(content)
                else:
                    continue
            else:
                print(f"Size of tweet exceeded max: {len(content)}\n{paper['link']}\n{content}")
                continue
    else:
        print("No new Google Scholar papers.")
        
    # Save scraped_papers
    past_papers = pd.read_csv("data/scholar_papers.csv")
    past_papers = pd.concat([relevant_papers, past_papers])
    past_papers = past_papers[~past_papers['result_id'].duplicated()]
    past_papers = past_papers[~past_papers['title'].duplicated()]
    past_papers.to_csv("data/scholar_papers.csv", index=False)
    
    
if __name__ == "__main__":
    main(
        last_search = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d'),
        end_date = datetime.today().strftime('%Y-%m-%d')
    )

