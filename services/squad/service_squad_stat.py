import json
import os
from fastapi import HTTPException
from services.config import TEMP_DIR
from utils.get_season_id import get_season_file_by_id

def get_squad_stat(id: int, tag: str):
    file_name = get_season_file_by_id(id)
    file_path = os.path.join(TEMP_DIR, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Файл {file_name} не найден в папке temp")

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
            "missions_played": squad.get("missions_played",0),
            "score" : squad.get("score", 0)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении {file_name}: {str(e)}")
