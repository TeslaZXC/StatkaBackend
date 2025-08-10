import os
import json
import re
from fastapi import HTTPException
from services.config import STATS_FILE  

def get_team_players(tag: str):
    tag = tag.strip()

    if not os.path.exists(STATS_FILE):
        raise HTTPException(status_code=404, detail="Файл stats.json не найден.")

    with open(STATS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Ошибка чтения stats.json")

    if "players" not in data:
        raise HTTPException(status_code=500, detail="Неверный формат файла stats.json")

    pattern_brackets = re.compile(r"^\[([^\]]+)\]")  
    pattern_prefix = re.compile(r"^([^.]+)\.")    

    filtered_players = []

    for player_name, stats in data["players"].items():
        tag_found = None

        m = pattern_brackets.match(player_name)
        if m:
            tag_found = m.group(1)
        else:
            m = pattern_prefix.match(player_name)
            if m:
                tag_found = m.group(1)

        if tag_found == tag:
            filtered_players.append({
                "name": player_name,
                "stats": stats
            })

    if not filtered_players:
        raise HTTPException(status_code=404, detail=f"Игроки с тегом '{tag}' не найдены.")

    return filtered_players
