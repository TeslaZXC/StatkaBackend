import os
import json
from fastapi import HTTPException
from services.config import TEMP_DIR  
from utils.get_season_id import get_season_file_by_id

def get_squad_top(id : int):
    try:
        file_name = get_season_file_by_id(id)

        file_path = os.path.join(TEMP_DIR, file_name)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Файл {file_name} не найден в папке temp.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        teams = data.get("teams")
        if not teams:
            raise HTTPException(status_code=404, detail="В файле отсутствует ключ 'teams'.")

        cleaned = {}
        for tag, stats in teams.items():
            cleaned[tag] = {k: v for k, v in stats.items() if k != "side"}

        return cleaned

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении {file_name}: {str(e)}")
