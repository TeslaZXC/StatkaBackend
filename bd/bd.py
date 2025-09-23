from pymongo import MongoClient

# Подключение к базе
client = MongoClient("mongodb://localhost:27017/")
db = client["stats"]

missions = db["mission_stat"]
ocap_tokens = db["ocap_tokens"]  
squads_collection = db["squads"]  # добавим коллекцию squads


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
        "win_side": 1,
        "players_count": 1   
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
    doc = squads_collection.find_one({}, {"_id": 0})
    return doc if doc else {}


def get_registered_squad_tags() -> set:
    """
    Возвращает множество тегов всех зарегистрированных отрядов
    """
    squads = get_all_squads()
    return set(squads.keys()) if squads else set()


def save_ocap_token(payload: dict):
    ocap_tokens.insert_one(payload)


def get_ocap_token(short_id: str):
    return ocap_tokens.find_one({"short_id": short_id}, {"_id": 0})


def find_ocap_token_by_ip_and_data(user_ip: str, data: dict):
    """
    Проверка, есть ли уже ссылка у пользователя с таким IP и данными
    """
    return ocap_tokens.find_one(
        {
            "user_ip": user_ip,
            "urlOcap": data["urlOcap"],
            "missionName": data["missionName"],
            "killName": data["killName"],
            "killerName": data["killerName"],
            "timeKill": data["timeKill"],
            "weapon": data["weapon"],
            "distance": data["distance"],
            "idMission": data["idMission"]
        },
        {"_id": 0}
    )
