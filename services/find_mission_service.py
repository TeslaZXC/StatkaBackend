from bd.bd import missions

def find_mission(file: str, file_date: str) -> dict | None:
    """
    Ищет миссию по полям file и file_date, возвращает её id
    """
    query = {
        "file": file,
        "file_date": file_date
    }
    projection = {"_id": 0, "id": 1}
    return missions.find_one(query, projection)
