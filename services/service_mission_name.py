from fastapi import HTTPException
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mission"]
collection = db["stat"]


def get_mission_info_by_id(mission_id: int) -> dict:
    doc_id = str(mission_id)

    mission_data = collection.find_one({"_id": doc_id})

    if mission_data is None:
        raise HTTPException(status_code=404, detail=f"Миссия с ID {mission_id} не найдена в базе данных.")

    mission_name = mission_data.get("mission_name")
    play_link = mission_data.get("play_link")

    if not mission_name or not play_link:
        raise HTTPException(status_code=500, detail="Отсутствует поле 'mission_name' или 'play_link'.")

    return {
        "mission_name": mission_name,
        "play_link": play_link
    }
