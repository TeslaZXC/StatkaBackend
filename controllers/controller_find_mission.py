from fastapi import HTTPException
from services.find_mission_service import find_mission

def fetch_find_mission(file: str, file_date: str) -> dict:
    mission = find_mission(file, file_date)
    if not mission:
        raise HTTPException(status_code=404, detail="Миссия не найдена")
    return mission
