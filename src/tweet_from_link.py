# Example usage: python3 src/tweet_from_link.py -l https://arxiv.org/abs/2408.06292

from generate_summary import generate_summary, get_abstract
from tweet import tweet, shorten_url
from scrape_scholar import scrape_text
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--link", help="URL of paper page.")

args = parser.parse_args()
link = args.link

def main(link):
    web_text = scrape_text(link)
    abstract = get_abstract(web_text)
    summary = generate_summary(abstract)
    
    if "**skip**" in summary:
        raise Exception("Couldn't identify abstract.")
    
    short_link = shorten_url(link)
    
    content = f"{summary} {short_link}"
    if len(content) <= 280:
        tweet(content)
    else:
        raise Exception(f"Size of tweet exceeded max: {len(content)}\n{short_link}\n{content}")
    
if __name__ == "__main__":
    main(link)