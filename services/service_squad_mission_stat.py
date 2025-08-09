import os
import json
from fastapi import HTTPException
from services.config import MISSION_DIR, STATS_FILE

def get_squad_statistics(mission_id: int):
    try:
        for filename in os.listdir(MISSION_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(MISSION_DIR, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                        # Проверка ID
                        if str(data.get("id")) == str(mission_id):
                            team_stats = data.get("team_stats")
                            if not team_stats:
                                raise HTTPException(
                                    status_code=404,
                                    detail=f"Статистика отрядов для миссии {mission_id} не найдена."
                                )
                            return team_stats
                except Exception as e:
                    print(f"Ошибка при чтении {filename}: {e}")

        raise HTTPException(
            status_code=404,
            detail=f"Миссия с ID {mission_id} не найдена."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")
