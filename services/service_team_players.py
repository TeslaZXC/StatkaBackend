import os
import json
import re
from fastapi import HTTPException
from services.config import TEMP_DIR

def get_team_players(file_name: str, tag: str):
    tag = tag.strip()
    file_path = os.path.join(TEMP_DIR, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Файл {file_name} не найден в папке temp.")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Ошибка чтения {file_name}")

    if "players" not in data:
        raise HTTPException(status_code=500, detail=f"Неверный формат файла {file_name}")

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
        raise HTTPException(status_code=404, detail=f"Игроки с тегом '{tag}' не найдены в файле {file_name}.")

    return filtered_players
