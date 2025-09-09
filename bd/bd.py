from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stats"]
missions = db["mission_stat"]

def get_all_missions():
    data = missions.find({}, {
        "_id": 0,
        "id": 1,                
        "file": 1,
        "file_date": 1,
        "game_type": 1,
        "duration_frames": 1,
        "duration_time": 1,  
        "missionName": 1,
        "worldName": 1,
        "win_side": 1
    })
    return list(data)

def get_mission_info(mission_id: int):
    data = missions.find_one({"id": mission_id}, {
        "_id": 0,
        "id": 1,              
        "file": 1,
        "file_date": 1,
        "game_type": 1,
        "duration_frames": 1,
        "duration_time": 1,  
        "missionName": 1,
        "worldName": 1,
        "win_side": 1
    })
    return data

def get_players_by_id(mission_id: int):
    data = missions.find_one({"id": mission_id}, {
        "_id": 0,
        "id": 1,              
        "players": 1
    })
    return data.get("players", []) if data else []

def get_squads_by_id(mission_id: int):
    data = missions.find_one({"id": mission_id}, {
        "_id": 0,
        "id": 1,              
        "squads": 1
    })
    return data.get("squads", []) if data else []

def get_all_squads():
    doc = db["squads"].find_one({}, {"_id": 0})  
    return doc if doc else {}
