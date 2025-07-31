import json
import os
from fastapi import HTTPException

SQUADS_FILE = "data/squads.json"

def get_squad_top():
    if not os.path.exists(SQUADS_FILE):
        raise HTTPException(status_code=404, detail="Файл со сквадами не найден.")

    try:
        with open(SQUADS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        cleaned = {
            squad: {
                k: v for k, v in stats.items() if k not in ["side", "players"]
            }
            for squad, stats in data.items()
        }
        return cleaned

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Ошибка разбора JSON.")