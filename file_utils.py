"""
This script defines some utility code to read and write content from/to files.
"""
from pathlib import Path
import json
import io

def load_examples(filepath: Path):
    with open(filepath, "r") as f:
        lines = f.readlines()
    
    return [json.loads(line) for line in lines]

def generate_jsonl(data):
    buffer = io.StringIO()
    for entry in data:
        buffer.write(json.dumps(entry) + "\n")
    return buffer.getvalue()