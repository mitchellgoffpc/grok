import os
import json
import hashlib
from tqdm import tqdm
from .query import query_with_prompt

# Helper functions

def get_project_root():
  current_dir = os.getcwd()
  while current_dir != '/':
    if os.path.isdir(os.path.join(current_dir, '.grok')):
      return current_dir
    current_dir = os.path.dirname(current_dir)
  return None

def list_files(path):
  return [
    os.path.join(root[len(path+'/'):], file)
      for root, dirs, files in os.walk(path)
      for file in files
      if '/.' not in root]

def get_expected_checksums(project_root):
  try:
    with open(os.path.join(project_root, '.grok', 'checksums.json'), 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return {}

def get_checksum(data):
  return hashlib.md5(data.encode('utf-8')).hexdigest()

def get_summary(fn, data):
  print(fn)
  return query_with_prompt('scan', fn=fn, contents=data)


# Main function

def scan(args):
  project_root = get_project_root()
  if project_root is None:
    project_root = os.getcwd()
    os.makedirs('.grok', exist_ok=True)
    print(f"Initialized grok index in {project_root}")

  os.makedirs(os.path.join(project_root, '.grok', 'index'), exist_ok=True)

  files = list_files(project_root)
  checksums = get_expected_checksums(project_root)
  mismatched_files = [f for f in files if get_checksum(f) != checksums.get(f)]

  # Scan mismatched files
  print(f"Scanning {len(mismatched_files)} files ...")

  summaries = {}
  for i, fn in enumerate(mismatched_files):
    with open(fn) as f:
      data = f.read()
    checksums[fn] = get_checksum(data)
    summary = get_summary(fn, data)
    with open(os.path.join(project_root, '.grok', 'index', fn.replace('/', '__')), 'w') as f:
      f.write(summary)
    with open(os.path.join(project_root, '.grok', 'checksums.json'), 'w') as f:
      json.dump(checksums, f)
