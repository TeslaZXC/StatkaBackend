import os
import json
from fastapi import HTTPException

PLAYER_FILE = "data/players.json"

def search_player_names(query: str) -> list[str]:
    if not os.path.exists(PLAYER_FILE):
        raise HTTPException(status_code=404, detail="Файл player.json не найден.")

    try:
        with open(PLAYER_FILE, "r", encoding="utf-8") as f:
            players = json.load(f)

        return [name for name in players if query.lower() in name.lower()]
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Ошибка разбора JSON.")