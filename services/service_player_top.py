from pymongo import MongoClient
from fastapi import HTTPException

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stat"]

players_col = db["players"]
teams_col = db["teams"]

def get_top_player():
    try:
        valid_teams = set(team["_id"] for team in teams_col.find({}, {"_id": 1}))

        cursor = players_col.find({
            "missions": {"$exists": True, "$not": {"$size": 0}},
            "$expr": {"$gt": [{"$size": "$missions"}, 20]},
            "squad": {"$in": list(valid_teams)}
        })

        players_stats = []
        for player in cursor:
            name = player.get("name", "Unknown")
            frags = player.get("frags", 0)
            deaths = player.get("deaths", 0)
            missions = player.get("missions", [])
            squad = player.get("squad", "")

            if deaths > 0:
                kd = round(frags / deaths, 2)
            elif frags > 0:
                kd = float(frags)
            else:
                kd = 0.0

            players_stats.append({
                "name": name,
                "squad": squad,
                "frags": frags,
                "deaths": deaths,
                "kd": kd,
                "missions": len(missions)
            })

        sorted_players = sorted(players_stats, key=lambda x: x["kd"], reverse=True)

        return sorted_players[:100]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при доступе к MongoDB: {str(e)}")
