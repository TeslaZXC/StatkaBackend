import json
import os
from fastapi import HTTPException

PLAYERS_FILE = "data/players.json"

def load_player_by_name(name: str):
    if not os.path.exists(PLAYERS_FILE):
        raise HTTPException(status_code=404, detail="Файл игроков не найден.")

    try:
        with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
            players = json.load(f)

        for player_name, data in players.items():
            if player_name.lower() == name.lower():
                return data

        raise HTTPException(status_code=404, detail=f"Игрок '{name}' не найден.")

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Ошибка разбора JSON.")
