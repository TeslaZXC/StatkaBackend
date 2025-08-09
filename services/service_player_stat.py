import os
import json
import re
from fastapi import HTTPException
from services.config import MISSION_DIR, STATS_FILE

def clean_name(name: str) -> str:
    """Удаляет теги и возвращает чистое имя игрока"""
    name = re.sub(r"\[.*?\]\s*", "", name)
    name = re.sub(r"^[A-Za-z0-9]+\.\s*", "", name)
    return name.strip().lower()

def load_player_by_name(name: str) -> dict:
    try:
        if not os.path.exists(STATS_FILE):
            raise HTTPException(status_code=404, detail="Файл stats.json не найден.")

        with open(STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        players = data.get("players")
        if not players:
            raise HTTPException(status_code=404, detail="В файле нет данных об игроках.")

        search_name = clean_name(name)

        for player_name, stats in players.items():
            if clean_name(player_name) == search_name:
                return stats

        raise HTTPException(status_code=404, detail=f"Игрок '{name}' не найден.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении stats.json: {str(e)}")
