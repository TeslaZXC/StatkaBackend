from fastapi import HTTPException
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mission"]
collection = db["squad"]

def get_squad_statistics(mission_id: int):
    try:
        doc_id = str(mission_id)
        document = collection.find_one({"_id": doc_id})

        if not document:
            raise HTTPException(status_code=404, detail=f"Статистика отрядов для миссии {mission_id} не найдена в базе данных.")

        document.pop("_id", None)

        return document

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при доступе к MongoDB: {str(e)}")
