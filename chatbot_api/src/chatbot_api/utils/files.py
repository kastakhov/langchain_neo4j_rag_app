from __future__ import annotations
from os import path
from pathlib import Path

DATA_DIR = path.join(path.dirname(__file__), "../data")

def get_template_from_file(filename: str) -> str:
    return Path(path.join(DATA_DIR, filename)).read_text()
