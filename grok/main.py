#!/usr/bin/env python3
import argparse
from .ask import ask

def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help='command', dest='command')
  scan_parser = subparsers.add_parser('scan')
  ask_parser = subparsers.add_parser('ask')

  parser.add_argument('-m', '--model', choices=['gpt-3.5-turbo', 'gpt-4'], default='gpt-3.5-turbo')
  scan_parser.add_argument('directory')
  ask_parser.add_argument('question', nargs='+')
  args = parser.parse_args()

  if args.command == 'scan':
    raise NotImplementedError()
  elif args.command == 'ask':
    ask(args)
