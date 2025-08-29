from fastapi import HTTPException
from bd.bd import missions
from datetime import datetime

def _parse_date(date_str: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%Y_%m_%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise HTTPException(status_code=400, detail=f"Неверный формат даты: {date_str}")

def _get_top_players_by_frag_type(start_date: str, end_date: str, frag_type: str):
    start_dt = _parse_date(start_date)
    end_dt = _parse_date(end_date)

    cursor = missions.find(
        {"file_date": {"$gte": start_date, "$lte": end_date}},
        {"_id": 0, "file_date": 1, "players": 1}
    )

    if missions.count_documents({"file_date": {"$gte": start_date, "$lte": end_date}}) == 0:
        raise HTTPException(status_code=404, detail="Миссии в указанном диапазоне не найдены")

    player_stats = {}

    for doc in cursor:
        file_date = _parse_date(doc.get("file_date"))
        for p in doc.get("players", []):
            name = p.get("name")
            if not name:
                continue

            frags = p.get(frag_type, 0)
            squad = p.get("squad")
            prev = player_stats.get(name, {})

            player_stats[name] = {
                "name": name,
                "frags": prev.get("frags", 0) + frags,
                "deaths": prev.get("deaths", 0) + p.get("death", 0),
                "missions_played": prev.get("missions_played", 0) + 1,
                # если squad есть и миссия новее — обновляем
                "squad": squad if squad and file_date >= prev.get("last_date", datetime.min) else prev.get("squad"),
                "last_date": max(file_date, prev.get("last_date", datetime.min))
            }

    players_list = []
    for stats in player_stats.values():
        if stats["missions_played"] <= 5 or not stats["squad"]:
            continue
        deaths = stats["deaths"] if stats["deaths"] > 0 else 1
        kd = round(stats["frags"] / deaths, 2)
        score = stats["frags"] / stats["missions_played"]
        players_list.append({
            "name": stats["name"],
            "frags": stats["frags"],
            "missions_played": stats["missions_played"],
            "deaths": stats["deaths"],
            "kd": kd,
            "score": score,
            "squad": stats["squad"]  # всегда последний отряд
        })

    players_list.sort(key=lambda x: x["score"], reverse=True)
    return players_list[:100]

def get_top_all_players_by_period(start_date: str, end_date: str):
    return _get_top_players_by_frag_type(start_date, end_date, "frags")

def get_top_inf_players_by_period(start_date: str, end_date: str):
    return _get_top_players_by_frag_type(start_date, end_date, "frags_inf")

def get_top_veh_players_by_period(start_date: str, end_date: str):
    return _get_top_players_by_frag_type(start_date, end_date, "frags_veh")
