import pandas as pd
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import yaml
import requests
from openai import OpenAI


with open('src/config.yml', 'r') as file:
    config = yaml.safe_load(file)
        
serpapi_key = config['serpapi']['API-key']
api_key = config['openai']['API-key']
client = OpenAI(api_key=api_key)


def scholar_search(searches):
  past_papers = pd.read_csv("data/scholar_papers.csv")
  relevant_papers = past_papers.iloc[0:]

  for query in searches:
    search = GoogleSearch({
        "engine": "google_scholar",
        "q": query,
        "scisbd" : 1,
        "as_vis" : 1,
        "api_key": serpapi_key
      })
    
    result = search.get_dict()
    relevant_papers = pd.concat([relevant_papers, pd.DataFrame(result['organic_results']).iloc[:, 1:]])
    
  relevant_papers = relevant_papers[~relevant_papers['result_id'].duplicated()]
  relevant_papers = relevant_papers[~relevant_papers['result_id'].isin(past_papers['result_id'])]

  return relevant_papers


def scrape_text(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(string=True)
    
    output = ''
    
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
            
    return output[:100000]


    



