import tweepy
import yaml

def tweet(text):

    with open('config.yml', 'r') as file:
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