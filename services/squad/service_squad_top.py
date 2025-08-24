from typing import List, Dict
from bd.bd import get_all_missions, get_squads_by_file

def get_squad_top_by_period(start_date: str, end_date: str) -> List[Dict]:
    missions = get_all_missions()

    missions_in_period = [
        m for m in missions 
        if start_date <= m.get("file_date", "") <= end_date
    ]

    squad_stats = {}

    for mission in missions_in_period:
        file_name = mission["file"]
        squads = get_squads_by_file(file_name)

        for squad in squads:
            tag = squad["squad_tag"]
            if tag not in squad_stats:
                squad_stats[tag] = {
                    "squad_tag": tag,
                    "frags": 0,
                    "death": 0,
                    "tk": 0,
                    "mission_play": 0,
                    "total_victims_players": 0  
                }

            squad_stats[tag]["frags"] += squad.get("frags", 0)
            squad_stats[tag]["death"] += squad.get("death", 0)
            squad_stats[tag]["tk"] += squad.get("tk", 0)
            squad_stats[tag]["mission_play"] += 1
            squad_stats[tag]["total_victims_players"] += len(squad.get("victims_players", []))

    for stats in squad_stats.values():
        stats["kd"] = round(stats["frags"] / stats["death"], 2) if stats["death"] > 0 else stats["frags"]
        stats["average_presence"] = round(stats["total_victims_players"] / stats["mission_play"], 2) if stats["mission_play"] > 0 else 0
        stats["score"] = round(
            (stats["frags"] / stats["mission_play"]) / stats["average_presence"], 2
        ) if stats["average_presence"] > 0 else 0
        del stats["total_victims_players"]

    top_squads = sorted(squad_stats.values(), key=lambda x: x["score"], reverse=True)

    return top_squads
