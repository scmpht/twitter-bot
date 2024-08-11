from openai import OpenAI
import yaml

with open('src/config.yml', 'r') as file:
    config = yaml.safe_load(file)
        
api_key = config['openai']['API-key']
prompt = config['openai']['prompt']

client = OpenAI(api_key=api_key)

def generate_summary(abstract):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": abstract},
        ]
    )
        
    return completion.choices[0].message.content