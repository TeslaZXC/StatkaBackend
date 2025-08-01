import os
import json
from fastapi import HTTPException

MISSIONS_FOLDER = "data/mission/stat"

def get_mission_list():
    if not os.path.exists(MISSIONS_FOLDER):
        raise HTTPException(status_code=404, detail="Папка с миссиями не найдена.")

    missions = []
    for filename in os.listdir(MISSIONS_FOLDER):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(MISSIONS_FOLDER, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                mission = json.load(f)
                missions.append(mission)
        except json.JSONDecodeError:
            continue
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при чтении {filename}: {str(e)}")

    missions.sort(key=lambda m: int(m.get("id", 0)), reverse=True)

    return missions