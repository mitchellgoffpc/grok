from ask.query import query

def ask(message, model):
  response = query(message, model)
  print(response)
