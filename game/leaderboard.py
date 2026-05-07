import json
import os

_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scores.json')


def load():
    try:
        with open(_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def save(lb):
    with open(_FILE, 'w') as f:
        json.dump(lb, f)
