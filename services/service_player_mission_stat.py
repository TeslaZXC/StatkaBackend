from fastapi import HTTPException
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mission"]
collection = db["player"]

def get_player_mission_stats(mission_id: int):
    doc_id = str(mission_id)

    try:
        data = collection.find_one({"_id": doc_id})
        if data is None:
            raise HTTPException(status_code=404, detail=f"Данные для миссии {mission_id} не найдены в базе.")

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к базе данных: {str(e)}")
