import os
import json
import re
from fastapi import HTTPException
from services.config import TEMP_DIR  # путь к папке temp

def clean_name(name: str) -> str:
    """Удаляет теги и возвращает чистое имя игрока"""
    name = re.sub(r"\[.*?\]\s*", "", name)
    name = re.sub(r"^[A-Za-z0-9]+\.\s*", "", name)
    return name.strip().lower()

def load_player_by_name(file_name: str, name: str) -> dict:
    try:
        file_path = os.path.join(TEMP_DIR, file_name)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Файл {file_name} не найден в папке temp.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        players = data.get("players")
        if not players:
            raise HTTPException(status_code=404, detail="В файле нет данных об игроках.")

        search_name = clean_name(name)

        for player_name, stats in players.items():
            if clean_name(player_name) == search_name:
                return stats

        raise HTTPException(status_code=404, detail=f"Игрок '{name}' не найден в файле {file_name}.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении {file_name}: {str(e)}")
