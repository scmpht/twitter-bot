import tweepy
import yaml
import requests


def shorten_url(long_url):
    url = 'http://tinyurl.com/api-create.php?url='
    response = requests.get(url+long_url)
    short_url = response.text
    
    return short_url


def tweet(text):

    with open('src/config.yml', 'r') as file:
        config = yaml.safe_load(file)
        
    bearer_token = config['twitter']['bearer-token']
    consumer_key = config['twitter']['API-key']
    consumer_secret = config['twitter']['API-key-secret']
    access_token = config['twitter']['access-token']
    access_token_secret = config['twitter']['access-token-secret']

    client = tweepy.Client(
        bearer_token, consumer_key, consumer_secret, access_token, access_token_secret
    )

    client.create_tweet(text=text)

    print(f"Tweeted: '{text}'")