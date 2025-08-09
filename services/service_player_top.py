import os
import json
from fastapi import HTTPException
from services.config import MISSION_DIR, STATS_FILE

def get_top_player():
    try:
        if not os.path.exists(STATS_FILE):
            raise HTTPException(status_code=404, detail="Файл stats.json не найден.")

        with open(STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        players = data.get("players")
        if not players:
            raise HTTPException(status_code=404, detail="В файле нет данных об игроках.")

        players_stats = []
        for name, stats in players.items():
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
