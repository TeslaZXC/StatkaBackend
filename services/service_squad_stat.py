import json
import os
from fastapi import HTTPException
from services.config import MISSION_DIR, STATS_FILE

def get_squad_stat(tag: str):
    file_path = STATS_FILE

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл stats.json не найден")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        teams = data.get("teams", {})
        tag_upper = tag.upper()

        if tag_upper not in teams:
            return None

        squad = teams[tag_upper]
        return {
            "name": tag_upper,
            "frags": squad.get("frags", 0),
            "teamkills": squad.get("teamkills", 0),
            "deaths": squad.get("deaths", 0),
            "side": squad.get("side", "unknown")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении stats.json: {str(e)}")
