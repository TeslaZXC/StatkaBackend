import json
import os

SQUADS_FILE = "data/squads.json"

def load_squad_data():
    if not os.path.exists(SQUADS_FILE):
        return {}
    with open(SQUADS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_squad_stat(tag: str):
    data = load_squad_data()
    tag_upper = tag.upper()
    squad = data.get(tag_upper)
    if not squad:
        return None

    return {
        "name": tag_upper,
        "frags": squad.get("frags", 0),
        "deaths": squad.get("deaths", 0),
        "average_attendance": squad.get("average_attendance", 0),
        "members": squad.get("members", []),
        "score":squad.get("score",0)
    }
