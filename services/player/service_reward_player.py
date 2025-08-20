import json
from typing import Optional
from services.config import REWARD_PLAYER

JSON_FILE = REWARD_PLAYER

def find_json_by_name(name: str) -> Optional[dict]:
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(name)  
    except (FileNotFoundError, json.JSONDecodeError):
        return None