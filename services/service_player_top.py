import os
import json
import re
from fastapi import HTTPException
from services.config import MISSION_DIR, STATS_FILE, TEAM_FILE

def load_team_list():
    if not os.path.exists(TEAM_FILE):
        raise HTTPException(status_code=404, detail="Файл team.json не найден.")
    with open(TEAM_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # Предполагаем, что в файле team.json список отрядов — например, ["LG", "DW", "ABC"]
            if isinstance(data, list):
                return data
            else:
                raise HTTPException(status_code=500, detail="Формат team.json некорректен.")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Ошибка при чтении team.json")

def get_top_player():
    try:
        if not os.path.exists(STATS_FILE):
            raise HTTPException(status_code=404, detail="Файл stats.json не найден.")

        # Загружаем список отрядов из team.json
        teams = load_team_list()

        with open(STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        players = data.get("players")
        if not players:
            raise HTTPException(status_code=404, detail="В файле нет данных об игроках.")

        # Регулярные выражения для поиска тега
        # 1) Квадратные скобки в начале: [LG]Nick
        pattern_brackets = re.compile(r"^\[([^\]]+)\]")
        # 2) Префикс с точкой: DW.Nick
        pattern_prefix = re.compile(r"^([^.]+)\.")

        players_stats = []
        for name, stats in players.items():
            # Проверяем тег
            tag = None

            m = pattern_brackets.match(name)
            if m:
                tag = m.group(1)
            else:
                m = pattern_prefix.match(name)
                if m:
                    tag = m.group(1)

            # Если тег отсутствует или не в списке команд - пропускаем игрока
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
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении stats.json: {str(e)}")
