import os
import json
import re
from fastapi import HTTPException
from services.config import MISSION_DIR

MISSION_TEMP_DIR = MISSION_DIR

def get_mission_squad_player_stat(mission_id: int, squad_tag: str):
    if not os.path.exists(MISSION_TEMP_DIR):
        raise HTTPException(status_code=404, detail="Папка с миссиями не найдена")

    mission_file = None
    for filename in os.listdir(MISSION_TEMP_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(MISSION_TEMP_DIR, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if str(data.get("id")) == str(mission_id):
                    mission_file = data
                    break
            except Exception:
                continue

    if not mission_file:
        raise HTTPException(status_code=404, detail=f"Миссия с id {mission_id} не найдена")

    players_stats = mission_file.get("players_stats", [])
    tag_clean = squad_tag.strip().lower()

    # Регулярки:
    tag_patterns = [
        rf"^\[{re.escape(tag_clean)}\]",  
        rf"^{re.escape(tag_clean)}\.",    
        rf"^{re.escape(tag_clean)}[\s]", 
        rf"^{re.escape(tag_clean)}$"     
    ]

    result = []
    for player in players_stats:
        name_lower = player.get("player_name", "").lower()

        if any(re.match(pat, name_lower, flags=re.IGNORECASE) for pat in tag_patterns):
            result.append({
                "player_name": player.get("player_name"),
                "frags": player.get("frags", 0),
                "teamkills": player.get("teamkills", 0),
                "deaths": 1 if player.get("death") else 0
            })

    return result
