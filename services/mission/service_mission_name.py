from fastapi import HTTPException
from pymongo import MongoClient
from bd.bd import get_mission_info

def get_mission_info_by_id(mission_id: int) -> dict:
    mission = get_mission_info(mission_id)  # вызываем функцию из твоего скрипта

    if not mission:
        raise HTTPException(
            status_code=404,
            detail=f"Миссия с ID {mission_id} не найдена."
        )

    # возвращаем только нужные поля
    return {
        "file": mission.get("file"),
        "worldName": mission.get("worldName")
    }