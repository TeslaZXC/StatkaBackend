import os
import json
from fastapi import HTTPException
from services.config import MISSION_DIR, STATS_FILE

def get_squad_top():
    try:
        if not os.path.exists(STATS_FILE):
            raise HTTPException(status_code=404, detail="Файл stats.json не найден.")

        with open(STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        teams = data.get("teams")
        if not teams:
            raise HTTPException(status_code=404, detail="В файле stats.json отсутствует ключ 'teams'.")

        cleaned = {}
        for tag, stats in teams.items():
            cleaned[tag] = {k: v for k, v in stats.items() if k != "side"}

        return cleaned

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении stats.json: {str(e)}")
