import os
import json
from fastapi import HTTPException

STAT_DIR = "data/mission/stat"

def get_mission_info_by_id(mission_id: int) -> dict:
    file_path = os.path.join(STAT_DIR, f"{mission_id}.json")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Файл миссии {mission_id} не найден.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            mission_data = json.load(f)

        mission_name = mission_data.get("mission_name")
        play_link = mission_data.get("play_link")

        if not mission_name or not play_link:
            raise HTTPException(status_code=500, detail="Отсутствует поле 'mission_name' или 'play_link'.")

        return {
            "mission_name": mission_name,
            "play_link": play_link
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Ошибка разбора JSON.")
