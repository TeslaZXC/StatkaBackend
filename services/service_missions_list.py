from fastapi import HTTPException
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mission"]
collection = db["stat"]


def get_mission_list():
    try:
        missions_cursor = collection.find({})

        missions = list(missions_cursor)

        missions.sort(key=lambda m: int(m.get("id", 0)), reverse=True)

        return missions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении миссий из базы данных: {str(e)}")
