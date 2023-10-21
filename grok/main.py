#!/usr/bin/env python3
import argparse
from ask.main import AVAILABLE_MODELS, DEFAULT_MODEL, MODEL_SHORTCUTS
from grok.ask import ask
from grok.scan import scan


def main():
    # Define a parser for the common arguments like --model
  common_parser = argparse.ArgumentParser(add_help=False)
  common_parser.add_argument('-m', '--model', choices=AVAILABLE_MODELS, default=DEFAULT_MODEL)

  # Define the main parser
  parser = argparse.ArgumentParser(parents=[common_parser])
  subparsers = parser.add_subparsers(help='command', dest='command')

  # Define the subparsers
  ask_parser = subparsers.add_parser('ask', parents=[common_parser])
  ask_parser.add_argument('question', nargs='+')
  scan_parser = subparsers.add_parser('scan', parents=[common_parser])
  scan_parser.add_argument('question', nargs='+')

  # Parse and dispatch
  args = parser.parse_args()
  model = MODEL_SHORTCUTS.get(args.model, args.model)

  if args.command == 'scan':
    scan(model)
  elif args.command == 'ask':
    question = ' '.join(args.question)
    ask(question, model)


if __name__ == '__main__':
  main()
