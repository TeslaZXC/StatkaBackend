from collections import Counter
from fastapi import HTTPException, APIRouter, Query
from datetime import datetime, timedelta
from bd.bd import missions

def _parse_date(date_str: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%Y_%m_%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise HTTPException(status_code=400, detail=f"Неверный формат даты: {date_str}")

def _get_week_key(date: datetime) -> str:
    weekday = date.weekday()
    offset = (weekday - 3) % 7
    week_start = date - timedelta(days=offset)
    week_end = week_start + timedelta(days=2)
    return week_start.strftime("%Y_%m_%d"), week_end.strftime("%Y_%m_%d")

def aggregate_player_stats_by_date(player_name: str, start_date: str, end_date: str, squad: str | None = None) -> dict:
    query = {"file_date": {"$gte": start_date, "$lte": end_date}}
    cursor = missions.find(query, {"_id": 0, "file": 1, "file_date": 1, "players": 1})

    if missions.count_documents(query) == 0:
        raise HTTPException(status_code=404, detail="Миссии в указанном диапазоне не найдены")

    total_stats = {
        "name": player_name,
        "squad_filter": squad,
        "start_date": start_date,
        "end_date": end_date,
        "matches": 0,
        "frags": 0,
        "frags_veh": 0,
        "frags_inf": 0,
        "tk": 0,
        "death": 0,
        "destroyed_veh": 0,
        "victims_players": [],
        "missions": [],
        "squads": set(),
        "weapons": Counter(),
        "vehicles": Counter(),
        "killed_players": Counter()
    }

    weekly_stats = {}

    for doc in cursor:
        file_date = _parse_date(doc["file_date"])
        week_start_str, week_end_str = _get_week_key(file_date)
        week_key = f"{week_start_str} - {week_end_str}"

        if week_key not in weekly_stats:
            weekly_stats[week_key] = {
                "matches": 0,
                "frags": 0,
                "frags_veh": 0,
                "frags_inf": 0,
                "tk": 0,
                "death": 0,
                "destroyed_veh": 0,
                "weapons": Counter(),
                "vehicles": Counter(),
                "killed_players": Counter(),
                "missions": []
            }
        w = weekly_stats[week_key]

        players = doc.get("players", [])
        for p in players:
            if p.get("name", "").lower() != player_name.lower():
                continue
            if squad and p.get("squad") != squad:
                continue

            total_stats["matches"] += 1
            total_stats["frags"] += p.get("frags", 0)
            total_stats["frags_veh"] += p.get("frags_veh", 0)
            total_stats["frags_inf"] += p.get("frags_inf", 0)
            total_stats["tk"] += p.get("tk", 0)
            total_stats["death"] += p.get("death", 0)
            total_stats["destroyed_veh"] += p.get("destroyed_veh", 0)

            squad_name = p.get("squad")
            if squad_name:
                total_stats["squads"].add(squad_name)

            total_stats["missions"].append({
                "file": doc["file"],
                "file_date": doc["file_date"],
                "frags": p.get("frags", 0),
                "frags_veh": p.get("frags_veh", 0),
                "frags_inf": p.get("frags_inf", 0),
                "tk": p.get("tk", 0),
                "death": p.get("death", 0),
                "destroyed_veh": p.get("destroyed_veh", 0),
                "squad": p.get("squad")
            })

            w["matches"] += 1
            w["frags"] += p.get("frags", 0)
            w["frags_veh"] += p.get("frags_veh", 0)
            w["frags_inf"] += p.get("frags_inf", 0)
            w["tk"] += p.get("tk", 0)
            w["death"] += p.get("death", 0)
            w["destroyed_veh"] += p.get("destroyed_veh", 0)

            for victim in p.get("victims_players", []):
                if victim.get("kill_type") != "tk":
                    victim_name = victim.get("name")
                    weapon = victim.get("weapon")
                    kill_type = victim.get("kill_type")
                    if victim_name:
                        total_stats["killed_players"][victim_name] += 1
                        w["killed_players"][victim_name] += 1
                    if weapon and kill_type:
                        if kill_type == "kill":
                            total_stats["weapons"][weapon] += 1
                            w["weapons"][weapon] += 1
                        elif kill_type == "veh":
                            total_stats["vehicles"][weapon] += 1
                            w["vehicles"][weapon] += 1

            w["missions"].append({
                "file": doc["file"],
                "file_date": doc["file_date"],
                "frags": p.get("frags", 0),
                "frags_veh": p.get("frags_veh", 0),
                "frags_inf": p.get("frags_inf", 0),
                "tk": p.get("tk", 0),
                "death": p.get("death", 0),
                "destroyed_veh": p.get("destroyed_veh", 0),
                "squad": p.get("squad")
            })

    if total_stats["matches"] == 0:
        raise HTTPException(status_code=404, detail=f"Игрок '{player_name}' не найден в указанном диапазоне")

    total_stats["squads"] = list(total_stats["squads"])
    total_stats["weapons"] = dict(sorted(total_stats["weapons"].items(), key=lambda x: x[1], reverse=True))
    total_stats["vehicles"] = dict(sorted(total_stats["vehicles"].items(), key=lambda x: x[1], reverse=True))
    total_stats["killed_players"] = dict(sorted(total_stats["killed_players"].items(), key=lambda x: x[1], reverse=True))

    deaths = total_stats["death"] if total_stats["death"] > 0 else 1
    total_stats["kd_ratio"] = round(total_stats["frags"] / deaths, 2)
    total_stats["kd_inf"] = round(total_stats["frags_inf"] / deaths, 2)
    total_stats["kd_veh"] = round(total_stats["frags_veh"] / deaths, 2)

    total_stats["favorite_weapon"] = (
        {"name": next(iter(total_stats["weapons"])), "kills": next(iter(total_stats["weapons"].values()))}
        if total_stats["weapons"] else None
    )
    total_stats["favorite_vehicle"] = (
        {"name": next(iter(total_stats["vehicles"])), "kills": next(iter(total_stats["vehicles"].values()))}
        if total_stats["vehicles"] else None
    )

    weekly_result = {}
    for week_key, w in weekly_stats.items():
        w["weapons"] = dict(sorted(w["weapons"].items(), key=lambda x: x[1], reverse=True))
        w["vehicles"] = dict(sorted(w["vehicles"].items(), key=lambda x: x[1], reverse=True))
        w["killed_players"] = dict(sorted(w["killed_players"].items(), key=lambda x: x[1], reverse=True))

        deaths = w["death"] if w["death"] > 0 else 1
        w["kd_ratio"] = round(w["frags"] / deaths, 2)
        w["kd_inf"] = round(w["frags_inf"] / deaths, 2)
        w["kd_veh"] = round(w["frags_veh"] / deaths, 2)

        weekly_result[week_key] = w

    total_stats["weekly"] = weekly_result
    return total_stats