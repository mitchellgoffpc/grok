import os
import json
import requests

def ask(args):
  model = args.model
  message = ' '.join(args.question)
  api_key = os.getenv('OPENAI_API_KEY')

  r = requests.post('https://api.openai.com/v1/chat/completions', headers={"Authorization": f"Bearer {api_key}"}, json={
    "model": model,
    "messages": [{"role": "user", "content": message}],
    "temperature": 0.7
  })

  result = r.json()
  if r.status_code != 200:
    print(json.dumps(result, indent=2))
    exit()
  if os.getenv("DEBUG"):
    print(json.dumps(result, indent=2))
  assert len(result['choices']) == 1, f"Expected exactly one choice, but got {len(result['choices'])}!"

  print(result['choices'][0]['message']['content'])
