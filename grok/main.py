#!/usr/bin/env python3
import os
import sys
import json
import requests

def main():
  model = os.getenv("MODEL", "gpt-3.5-turbo")
  message = sys.argv[1] if len(sys.argv) >= 2 else "Say this is a test!"

  r = requests.post('https://api.openai.com/v1/chat/completions', headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}, json={
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
