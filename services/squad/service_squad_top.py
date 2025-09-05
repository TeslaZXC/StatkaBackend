from typing import List, Dict
from bd.bd import get_all_missions, get_squads_by_id, get_all_squads

def get_squad_top_by_period(start_date: str, end_date: str) -> List[Dict]:
    missions = get_all_missions()

    missions_in_period = [
        m for m in missions
        if start_date <= m.get("file_date", "") <= end_date
    ]

    valid_squads_doc = get_all_squads()
    valid_squads = {k.lower(): v for k, v in valid_squads_doc.items() if k != "_id"}

    squad_stats = {}

    for mission in missions_in_period:
        mission_id = mission["id"]
        squads = get_squads_by_id(mission_id)

        for squad in squads:
            tag = squad.get("squad_tag")
            if not tag:
                continue

            tag_lower = tag.lower()
            if tag_lower not in valid_squads:
                continue

            if tag_lower not in squad_stats:
                squad_stats[tag_lower] = {
                    "squad_tag": tag_lower,
                    "frags": 0,
                    "death": 0,
                    "tk": 0,
                    "mission_play": 0,
                    "total_victims_players": 0
                }

            squad_stats[tag_lower]["frags"] += squad.get("frags", 0)
            squad_stats[tag_lower]["death"] += squad.get("death", 0)
            squad_stats[tag_lower]["tk"] += squad.get("tk", 0)
            squad_stats[tag_lower]["mission_play"] += 1
            squad_stats[tag_lower]["total_victims_players"] += len(squad.get("victims_players", []))

    for stats in squad_stats.values():
        deaths = stats["death"] if stats["death"] > 0 else 1
        kd = round(stats["frags"] / deaths, 2)

        avg_presence = stats["total_victims_players"] / stats["mission_play"] if stats["mission_play"] > 0 else 0

        if avg_presence == 0 or stats["mission_play"] == 0:
            score = 0
        else:
            score = round(kd * (stats["frags"] / (stats["mission_play"] * avg_presence)), 3)

        stats["kd"] = kd
        stats["average_presence"] = round(avg_presence, 2)
        stats["score"] = score

        del stats["total_victims_players"]

    top_squads = sorted(squad_stats.values(), key=lambda x: x["score"], reverse=True)

    return top_squads
