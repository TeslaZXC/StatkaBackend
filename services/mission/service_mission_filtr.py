from typing import List, Dict
from bd.bd import get_all_missions

def get_mission_filtr() -> dict:
    missions = get_all_missions()

    game_types = set()
    win_sides = set()
    world_names = set()
    mission_names = set()

    for m in missions:
        gtype = m.get("game_type")
        if gtype not in ("tvt1", "tvt2"): 
            continue

        if gtype:
            game_types.add(gtype)
        if m.get("win_side"):
            win_sides.add(m["win_side"])
        if m.get("worldName"):
            world_names.add(m["worldName"])
        if m.get("missionName"):
            mission_names.add(m["missionName"])

    return {
        "game_types": sorted(game_types),
        "win_sides": sorted(win_sides),
        "world_names": sorted(world_names),
        "mission_names": sorted(mission_names),
    }