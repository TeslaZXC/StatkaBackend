from typing import Optional
from bd.bd import get_all_missions

def get_mission_list(
    game_type: Optional[str] = None,
    win_side: Optional[str] = None,
    world_name: Optional[str] = None,
    mission_name: Optional[str] = None,
    file_date: Optional[str] = None
):
    missions = get_all_missions()

    filters = {
        "game_type": game_type,
        "win_side": win_side,
        "worldName": world_name,
        "missionName": mission_name,
        "file_date": file_date
    }

    for key, value in filters.items():
        if value:
            if key == "missionName":
                missions = [m for m in missions if value.lower() in m.get(key, "").lower()]
            else:
                missions = [m for m in missions if m.get(key) == value]

    return missions
