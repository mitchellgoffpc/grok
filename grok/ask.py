import os
import json
import requests
from .query import query

def ask(args):
  message = ' '.join(args.question)
  print(query(message, model=args.model))
