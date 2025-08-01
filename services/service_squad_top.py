from fastapi import HTTPException
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stat"]
collection = db["squads"]

def get_squad_top():
    try:
        squads = collection.find()
        cleaned = {}

        for squad in squads:
            tag = squad["_id"]
            stats = {
                k: v for k, v in squad.items()
                if k not in ["_id", "side", "players"]
            }
            cleaned[tag] = stats

        return cleaned

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при доступе к MongoDB: {str(e)}")
