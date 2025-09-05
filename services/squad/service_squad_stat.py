from collections import Counter
from fastapi import HTTPException
from bd.bd import missions
from datetime import datetime

def _parse_date(date_str: str) -> datetime:
    try:
        date_str = date_str.replace("_", "-")
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Неверный формат даты: {date_str}, ожидался YYYY_MM_DD")


def get_squad_stat_by_period(squad_tag: str, start_date: str, end_date: str):
    start_dt = _parse_date(start_date)
    end_dt = _parse_date(end_date)

    cursor = missions.find(
        {"file_date": {"$gte": start_date, "$lte": end_date}},
        {"_id": 0, "file": 1, "file_date": 1, "squads": 1, "players": 1}
    )

    squad_stats = {
        "name": squad_tag,
        "frags": 0,
        "death": 0,
        "tk": 0,
        "missions_played": 0,
        "total_players": 0,
        "score": 0,
        "missions": [],
        "players_squad": {}
    }

    for doc in cursor:
        squads = doc.get("squads", [])
        squad_info = next((s for s in squads if s.get("squad_tag") == squad_tag), None)
        if not squad_info:
            continue

        squad_stats["missions_played"] += 1
        squad_stats["frags"] += squad_info.get("frags", 0)
        squad_stats["death"] += squad_info.get("death", 0)
        squad_stats["tk"] += squad_info.get("tk", 0)
        squad_stats["total_players"] = max(
            squad_stats["total_players"], len(squad_info.get("squad_players", []))
        )
        squad_stats["score"] += squad_info.get("frags", 0)

        squad_stats["missions"].append({
            "file": doc["file"],
            "file_date": doc["file_date"],
            "frags": squad_info.get("frags", 0),
            "death": squad_info.get("death", 0),
            "tk": squad_info.get("tk", 0),
            "total_players": len(squad_info.get("squad_players", [])),
            "squad_players": squad_info.get("squad_players", []),
            "victims_players": squad_info.get("victims_players", [])
        })

        for p in doc.get("players", []):
            if p.get("squad") != squad_tag:
                continue

            name = p.get("name")
            if not name:
                continue

            if name not in squad_stats["players_squad"]:
                squad_stats["players_squad"][name] = {
                    "name": name,
                    "squad": squad_tag,
                    "start_date": start_date,
                    "end_date": end_date,
                    "matches": 0,
                    "frags": 0,
                    "frags_inf": 0,
                    "frags_veh": 0,
                    "tk": 0,
                    "death": 0,
                    "destroyed_veh": 0,
                    "kd_ratio": 0.0,
                    "kd_inf": 0.0,
                    "kd_veh": 0.0
                }

            ps = squad_stats["players_squad"][name]
            ps["matches"] += 1
            ps["frags"] += p.get("frags", 0)
            ps["frags_inf"] += p.get("frags_inf", 0)
            ps["frags_veh"] += p.get("frags_veh", 0)
            ps["tk"] += p.get("tk", 0)
            ps["death"] += p.get("death", 0)
            ps["destroyed_veh"] += p.get("destroyed_veh", 0)

    if squad_stats["missions_played"] == 0:
        raise HTTPException(status_code=404, detail=f"Squad '{squad_tag}' не найден в указанном периоде")

    for ps in squad_stats["players_squad"].values():
        deaths = ps["death"] if ps["death"] > 0 else 1
        ps["kd_ratio"] = round(ps["frags"] / deaths, 2)
        ps["kd_inf"] = round(ps["frags_inf"] / deaths, 2)
        ps["kd_veh"] = round(ps["frags_veh"] / deaths, 2)

    squad_stats["players_squad"] = list(squad_stats["players_squad"].values())

    return squad_stats
