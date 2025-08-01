from pymongo import MongoClient
from fastapi import HTTPException

client = MongoClient("mongodb://localhost:27017/")
db = client["stat"]
collection = db["squads"]

def get_squad_stat(tag: str):
    tag_upper = tag.upper()

    try:
        squad = collection.find_one({"_id": tag_upper})
        if not squad:
            return None

        return {
            "name": tag_upper,
            "frags": squad.get("frags", 0),
            "deaths": squad.get("deaths", 0),
            "average_attendance": squad.get("average_attendance", 0),
            "members": squad.get("members", []),
            "score": squad.get("score", 0)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обращении к MongoDB: {str(e)}")
