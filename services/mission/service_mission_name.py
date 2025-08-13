import os
import json
from fastapi import HTTPException
from services.config import MISSION_DIR

def get_mission_info_by_id(mission_id: int) -> dict:
    folder_path = MISSION_DIR
    mission_id_str = str(mission_id)

    required_fields = [
        "id",
        "mission_name",
        "ocap_link",
        "stats_url",
        "players",
        "frags",
        "tk",
        "map",
        "duration",
        "date",
        "tag_check"
    ]

    if not os.path.exists(folder_path):
        raise HTTPException(status_code=500, detail=f"Папка с миссиями не найдена: {folder_path}")

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, dict) and data.get("id") == mission_id_str:
                    result = {field: data.get(field) for field in required_fields}
                    return result

            except Exception as e:
                print(f"Ошибка при чтении файла {file_path}: {e}")

    raise HTTPException(status_code=404, detail=f"Миссия с ID {mission_id} не найдена в файлах.")
