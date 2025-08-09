import json
import os
from fastapi import HTTPException
from services.config import MISSION_DIR, STATS_FILE

def search_player_names(query: str) -> list[str]:
    file_path = STATS_FILE
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл stats.json не найден")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        players = data.get("players", {})
        query_lower = query.lower()

        matching_names = [name for name in players if query_lower in name.lower()]

        return matching_names

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении stats.json: {str(e)}")
