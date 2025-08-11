import os
import json
import re
from fastapi import HTTPException
from services.config import TEMP_DIR, TEAM_FILE  # используем TEMP_DIR вместо STATS_FILE

def load_team_list():
    if not os.path.exists(TEAM_FILE):
        raise HTTPException(status_code=404, detail="Файл team.json не найден.")
    with open(TEAM_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                raise HTTPException(status_code=500, detail="Формат team.json некорректен.")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Ошибка при чтении team.json")

def normalize_tag(tag: str, teams: list):
    """Возвращает тег в том же виде, как он записан в team.json"""
    tag_lower = tag.lower()
    for team in teams:
        if team.lower() == tag_lower:
            return team
    return tag

def get_top_player(file_name: str):
    try:
        file_path = os.path.join(TEMP_DIR, file_name)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Файл {file_name} не найден в папке temp.")

        teams = load_team_list()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        players = data.get("players")
        if not players:
            raise HTTPException(status_code=404, detail="В файле нет данных об игроках.")

        pattern_brackets = re.compile(r"^\[([^\]]+)\]")
        pattern_prefix = re.compile(r"^([^.]+)\.")

        players_stats = []
        for name, stats in players.items():
            tag = None

            m = pattern_brackets.match(name)
            if m:
                tag = m.group(1)
            else:
                m = pattern_prefix.match(name)
                if m:
                    tag = m.group(1)

            if tag:
                tag = normalize_tag(tag.strip(), teams)

            if not tag or tag not in teams:
                continue

            frags = stats.get("frags", 0)
            deaths = stats.get("deaths_count", 0)

            if deaths > 0:
                kd = round(frags / deaths, 2)
            elif frags > 0:
                kd = float(frags)
            else:
                kd = 0.0

            players_stats.append({
                "name": name,
                "stats": stats,
                "kd": kd
            })

        sorted_players = sorted(players_stats, key=lambda x: x["kd"], reverse=True)

        return sorted_players[:100]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении {file_name}: {str(e)}")
