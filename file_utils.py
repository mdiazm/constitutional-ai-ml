"""
This script defines some utility code to read and write content from/to files.
"""
import io
import json
from pathlib import Path
from typing import Dict, List


def load_examples(filepath: Path) -> List[Dict]:
    """
    Load dict entries from json file.

    Args:
        filepath (Path): path to the JSON file.
    
    Returns:
        List[Dict]: list with dict entries from the JSON file.
    """
    with open(filepath, "r") as f:
        lines = f.readlines()
    
    return [json.loads(line) for line in lines]


def generate_jsonl(data: List[Dict]) -> io.StringIO:
    """
    Generate a buffer of json entries.

    Args:
        data (List): list of dict elements to write to the buffer

    Returns:
        io.StringIO: buffer with the written json entries.
    """
    buffer = io.StringIO()
    for entry in data:
        buffer.write(json.dumps(entry) + "\n")
    return buffer.getvalue()
