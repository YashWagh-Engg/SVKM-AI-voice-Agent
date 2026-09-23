import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_college_info():
    file_path = DATA_DIR / "college_info.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_responses():
    file_path = DATA_DIR / "responses.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)