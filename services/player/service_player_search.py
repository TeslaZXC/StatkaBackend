from fastapi import HTTPException
from datetime import datetime
from bd.bd import missions

def _parse_date(date_str: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%Y_%m_%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise HTTPException(status_code=400, detail=f"Неверный формат даты: {date_str}")

def search_player_names(query: str, start_date: str, end_date: str) -> list[str]:
    query_db = {"file_date": {"$gte": start_date, "$lte": end_date}}
    cursor = missions.find(query_db, {"_id": 0, "file_date": 1, "players": 1})

    if missions.count_documents(query_db) == 0:
        raise HTTPException(status_code=404, detail="Миссии в указанном диапазоне не найдены")

    start = _parse_date(start_date)
    end = _parse_date(end_date)
    query_lower = query.lower()

    found_names = set()

    for doc in cursor:
        try:
            file_date = _parse_date(doc["file_date"])
        except:
            continue
        if not (start <= file_date <= end):
            continue

        for p in doc.get("players", []):
            name = p.get("name", "")
            if query_lower in name.lower():
                found_names.add(name)

    if not found_names:
        raise HTTPException(status_code=404, detail=f"Игроки по запросу '{query}' не найдены")

    return sorted(found_names)
