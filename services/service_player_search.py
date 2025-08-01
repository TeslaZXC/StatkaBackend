from fastapi import HTTPException
from pymongo import MongoClient
import re

client = MongoClient("mongodb://localhost:27017/")
db = client["stat"]
collection = db["players"]

def search_player_names(query: str) -> list[str]:
    try:
        regex = re.compile(re.escape(query), re.IGNORECASE)

        cursor = collection.find({"name": {"$regex": regex}}, {"name": 1})

        return [doc["name"] for doc in cursor if "name" in doc]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к базе данных: {str(e)}")
