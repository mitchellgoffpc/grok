from grok.query import query

def ask(args):
  message = ' '.join(args.question)
  response = query(message, model=args.model)
  print(response)
