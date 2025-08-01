from fastapi import HTTPException
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stat"]
collection = db["players"]

def load_player_by_name(name: str) -> dict:
    try:
        player = collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})

        if not player:
            raise HTTPException(status_code=404, detail=f"Игрок '{name}' не найден.")

        player.pop("_id", None)

        return player

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при доступе к базе данных: {str(e)}")
