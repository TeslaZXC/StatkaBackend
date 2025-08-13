import os
import json
from fastapi import HTTPException
from services.config import MISSION_DIR

def get_player_mission_stats(mission_id: int):
    try:
        for filename in os.listdir(MISSION_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(MISSION_DIR, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                        if str(data.get("id")) == str(mission_id):
                            return data.get("players_stats", [])
                except Exception as e:
                    print(f"Ошибка при чтении {filename}: {e}")

        raise HTTPException(status_code=404, detail=f"Данные для миссии {mission_id} не найдены.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")
