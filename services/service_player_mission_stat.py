import os
import json
from fastapi import HTTPException

PLAYER_FOLDER = "data/mission/player"

def get_player_mission_stats(mission_id: int):
    file_path = os.path.join(PLAYER_FOLDER, f"{mission_id}.json")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Файл для миссии {mission_id} не найден.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Ошибка при разборе JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении файла: {str(e)}")