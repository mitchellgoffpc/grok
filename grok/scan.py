import os
import json
import hashlib
from grok.query import query_with_prompt

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
      if '/.' not in root and not file.startswith('.')]

def get_expected_checksums(project_root):
  try:
    with open(os.path.join(project_root, '.grok', 'checksums.json'), 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return {}

def get_checksum(fn):
  with open(fn, 'rb') as f:
    return hashlib.md5(f.read()).hexdigest()

def get_summary(fn):
  with open(fn) as f:
    return query_with_prompt('scan', fn=fn, contents=f.read())


# Main function

def scan(_):
  project_root = get_project_root()
  if project_root is None:
    project_root = os.getcwd()
    os.makedirs('.grok', exist_ok=True)
    print(f"Initialized grok index in {project_root}")

  os.makedirs(os.path.join(project_root, '.grok', 'index'), exist_ok=True)

  files = list_files(project_root)
  checksums = get_expected_checksums(project_root)
  mismatched_files = [fn for fn in files if get_checksum(fn) != checksums.get(fn)]

  # Scan mismatched files
  print(f"Scanning {len(mismatched_files)} files ...")

  for fn in mismatched_files:
    print(fn)
    checksums[fn] = get_checksum(fn)
    summary = get_summary(fn)
    with open(os.path.join(project_root, '.grok', 'index', fn.replace('/', '__')), 'w') as f:
      f.write(summary)
    with open(os.path.join(project_root, '.grok', 'checksums.json'), 'w') as f:
      json.dump(checksums, f, indent=2)
