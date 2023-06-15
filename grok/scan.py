import os
import json
import hashlib
from tqdm import tqdm

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
    with open(os.path.join(project_root, '.grok', 'checksums'), 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return {}

def get_checksum(file):
  with open(file, 'rb') as f:
    return hashlib.md5(f.read()).hexdigest()

def get_summary(file):
  import time; time.sleep(0.25)
  return "garbage"


# Main function

def scan(args):
  project_root = get_project_root()
  if project_root is None:
    project_root = os.getcwd()
    os.makedirs('.grok', exist_ok=True)
    print(f"Initialized grok index in {project_root}")

  files = list_files(project_root)
  checksums = get_expected_checksums(project_root)
  mismatched_files = [f for f in files if get_checksum(f) != checksums.get(f)]

  # Scan mismatched files
  print(f"Scanning {len(mismatched_files)} files ...")

  summaries = {}
  for i, f in enumerate(mismatched_files):
    print(f)
    checksums[f] = get_checksum(f)
    summary = get_summary(f)
    with open(os.path.join(project_root, '.grok', f.replace('/', '__')), 'w') as f:
      f.write(summary)

  with open(os.path.join(project_root, '.grok', 'checksums'), 'w') as f:
    json.dump(checksums, f)
