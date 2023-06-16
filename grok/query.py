import os
import json
import requests

def query_with_prompt(name, **kwargs):
  with open(os.path.join(os.path.dirname(__file__), 'prompts', f'{name}.txt')) as f:
    prompt = f.read()
    prompt = prompt.format(**kwargs)
  return query(prompt)

def query(message, model='gpt-3.5-turbo'):
  api_key = os.getenv('OPENAI_API_KEY')
  headers = {"Authorization": f"Bearer {api_key}"}
  params = {
    "model": model,
    "messages": [{"role": "user", "content": message}],
    "temperature": 0.7}

  r = requests.post('https://api.openai.com/v1/chat/completions', timeout=60, headers=headers, json=params)

  result = r.json()
  if r.status_code != 200:
    print(json.dumps(result, indent=2))
    raise RuntimeError("Invalid response from API")
  if os.getenv("DEBUG"):
    print(json.dumps(result, indent=2))
  assert len(result['choices']) == 1, f"Expected exactly one choice, but got {len(result['choices'])}!"

  return result['choices'][0]['message']['content']
