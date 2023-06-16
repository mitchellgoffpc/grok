#!/usr/bin/env python3
import argparse
from grok.ask import ask
from grok.scan import scan

def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help='command', dest='command')
  ask_parser = subparsers.add_parser('ask')
  subparsers.add_parser('scan')

  parser.add_argument('-m', '--model', choices=['gpt-3.5-turbo', 'gpt-4'], default='gpt-3.5-turbo')
  ask_parser.add_argument('question', nargs='+')
  args = parser.parse_args()

  if args.command == 'scan':
    scan(args)
  elif args.command == 'ask':
    ask(args)
