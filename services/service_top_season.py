import os
import json
import re
from fastapi import HTTPException
from services.config import TEMP_DIR, TEAM_FILE

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
    tag_lower = tag.lower()
    for team in teams:
        if team.lower() == tag_lower:
            return team
    return tag

def get_top_season(file_name: str):
    try:
        file_path = os.path.join(TEMP_DIR, file_name)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Файл {file_name} не найден в папке temp.")

        teams_list = load_team_list()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        players = data.get("players", {})
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
                tag = normalize_tag(tag.strip(), teams_list)

            if not tag or tag not in teams_list:
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

        top_players = sorted(players_stats, key=lambda x: x["kd"], reverse=True)[:3]
        teams_data = data.get("teams", {})
        if not teams_data:
            raise HTTPException(status_code=404, detail="В файле отсутствует ключ 'teams'.")

        squads_stats = []
        for tag, stats in teams_data.items():
            squad_frags = stats.get("frags", 0)
            squad_deaths = stats.get("deaths", 0)

            if squad_deaths > 0:
                kd = round(squad_frags / squad_deaths, 2)
            elif squad_frags > 0:
                kd = float(squad_frags)
            else:
                kd = 0.0

            cleaned_stats = {k: v for k, v in stats.items() if k != "side"}
            squads_stats.append({
                "tag": tag,
                "stats": cleaned_stats,
                "kd": kd
            })

        top_squads = sorted(squads_stats, key=lambda x: x["kd"], reverse=True)[:3]

        return {
            "top_players": top_players,
            "top_squads": top_squads
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении {file_name}: {str(e)}")
