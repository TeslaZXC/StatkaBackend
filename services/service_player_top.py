import json
import os

PLAYERS_FILE = "data/players.json"
TEAM_FILE = "data/team.json"

def get_top_player():
    if not os.path.exists(PLAYERS_FILE) or not os.path.exists(TEAM_FILE):
        return []

    with open(TEAM_FILE, "r", encoding="utf-8") as f:
        valid_teams = set(json.load(f).keys())

    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        players_data = json.load(f)

    players_stats = []

    for player in players_data.values():
        name = player.get("name", "Unknown")
        frags = player.get("frags", 0)
        deaths = player.get("deaths", 0)
        missions = player.get("missions", [])
        squad = player.get("squad", "")

        if len(missions) <= 20 or squad not in valid_teams:
            continue

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
