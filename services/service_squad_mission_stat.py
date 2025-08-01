import os
import json
from fastapi import HTTPException

SQUAD_FOLDER = "data/mission/squad"

def get_squad_statistics(mission_id: int):
    file_path = os.path.join(SQUAD_FOLDER, f"{mission_id}.json")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Файл статистики отрядов для миссии {mission_id} не найден.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Ошибка разбора JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении файла: {str(e)}")