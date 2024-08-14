from openai import OpenAI
import yaml
import time

with open('src/config.yml', 'r') as file:
    config = yaml.safe_load(file)
        
api_key = config['openai']['API-key']
twitter_prompt = config['openai']['twitter-prompt']
scrape_prompt = config['openai']['scrape-prompt']

client = OpenAI(api_key=api_key)


def generate_summary(abstract, max_attempts=4):
    
    attempts = 0
    while attempts < max_attempts:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = [
                {"role": "system", "content": twitter_prompt},
                {"role": "user", "content": abstract},
            ]
        )
        time.sleep(30)
        
        summary = completion.choices[0].message.content
        
        if len(summary) <= 252:
            return summary
        
        attempts += 1
    
    return summary


def get_abstract(text):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": scrape_prompt},
            {"role": "user", "content": text},
        ]
    ) 
    time.sleep(30)
    
    return completion.choices[0].message.content