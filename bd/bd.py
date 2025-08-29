from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stats"]
missions = db["mission_stat"]


def get_all_missions():
    """Возвращает все миссии с базовой информацией"""
    data = missions.find({}, {
        "_id": 0,
        "file": 1,
        "file_date": 1,
        "game_type": 1,
        "duration_frames": 1,
        "missionName": 1,
        "worldName": 1,
        "win_side": 1
    })
    return list(data)


def get_mission_info(file_name: str):
    data = missions.find_one({"file": file_name}, {
        "_id": 0,
        "file": 1,
        "file_date": 1,
        "game_type": 1,
        "duration_frames": 1,
        "missionName": 1,
        "worldName": 1,
        "win_side": 1
    })
    return data


def get_players_by_file(file_name: str):
    data = missions.find_one({"file": file_name}, {"_id": 0, "players": 1})
    return data.get("players", []) if data else []


def get_squads_by_file(file_name: str):
    data = missions.find_one({"file": file_name}, {"_id": 0, "squads": 1})
    return data.get("squads", []) if data else []

def get_all_squads():
    doc = db["squads"].find_one({}, {"_id": 0})
    return doc if doc else {}