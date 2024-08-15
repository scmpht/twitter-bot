from openai import OpenAI
import yaml
import time

with open('src/config.yml', 'r') as file:
    config = yaml.safe_load(file)
        
api_key = config['openai']['API-key']
twitter_prompt = config['openai']['twitter-prompt']
scrape_prompt = config['openai']['scrape-prompt']
verify_prompt = config['openai']['verify-prompt']


def generate_summary(abstract, max_attempts=5):
    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": twitter_prompt},
        {"role": "user", "content": abstract},
    ]
    
    attempts = 0
    while attempts < max_attempts:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = messages
        )
        time.sleep(30)
        
        summary = completion.choices[0].message.content
        
        if len(summary) <= 252:
            return summary
        
        messages.append(
            {"role": "assistant", "content": summary}
        )
        messages.append(
            {"role": "user", "content": f"Make this more concise, remove at least 15 words."}
        )
        
        attempts += 1
    
    return summary


def get_abstract(text):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": scrape_prompt},
            {"role": "user", "content": text},
        ]
    ) 
    time.sleep(30)
    
    return completion.choices[0].message.content


def verify_tweet(title, content):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": verify_prompt},
            {"role": "user", "content": f"Paper title: {title}\nSummary tweet: {content}"},
        ]
    ) 
    time.sleep(30)
    
    return completion.choices[0].message.content