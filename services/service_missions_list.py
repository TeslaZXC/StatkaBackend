import os
import json
from fastapi import APIRouter, HTTPException
from services.config import MISSION_DIR, STATS_FILE

router = APIRouter()

@router.get("/missions")
def get_mission_list():
    try:
        missions = []

        for filename in os.listdir(MISSION_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(MISSION_DIR, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                        mission_info = {
                            "id": data.get("id"),
                            "mission_name": data.get("mission_name"),
                            "ocap_link": data.get("ocap_link"),
                            "stats_url": data.get("stats_url"),
                            "players": data.get("players"),
                            "frags": data.get("frags"),
                            "tk": data.get("tk"),
                            "map": data.get("map"),
                            "duration": data.get("duration"),
                            "date": data.get("date"),
                            "tag_check": data.get("tag_check")
                        }

                        missions.append(mission_info)
                except Exception as e:
                    print(f"Ошибка при чтении {filename}: {e}")

        missions.sort(key=lambda m: int(m.get("id", 0)), reverse=True)

        return missions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении миссий: {str(e)}")
