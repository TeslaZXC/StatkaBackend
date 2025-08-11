import json
import os
from fastapi import HTTPException
from services.config import TEMP_DIR

def search_player_names(file_name: str, query: str) -> list[str]:
    file_path = os.path.join(TEMP_DIR, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Файл {file_name} не найден в папке temp")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        players = data.get("players", {})
        query_lower = query.lower()

        matching_names = [name for name in players if query_lower in name.lower()]

        return matching_names

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении {file_name}: {str(e)}")
