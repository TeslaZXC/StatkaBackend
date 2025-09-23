from typing import Optional
from bd.bd import get_all_missions

def get_mission_list(
    game_type: Optional[str] = None,
    win_side: Optional[str] = None,
    world_name: Optional[str] = None,
    mission_name: Optional[str] = None,
    file_date: Optional[str] = None,
    page: int = 1,               # по умолчанию 1
    per_page: int = 10           # по умолчанию 10
):
    missions = get_all_missions()

    # Фильтрация
    if game_type:
        if game_type.lower() == "tvt":
            missions = [m for m in missions if m.get("game_type") in ("tvt1", "tvt2")]
        else:
            missions = [m for m in missions if m.get("game_type") == game_type]

    if win_side:
        missions = [m for m in missions if m.get("win_side") == win_side]

    if world_name:
        missions = [m for m in missions if m.get("worldName") == world_name]

    if mission_name:
        missions = [m for m in missions if mission_name.lower() in m.get("missionName", "").lower()]

    if file_date:
        missions = [m for m in missions if m.get("file_date") == file_date]

    # Преобразование
    result = []
    for m in missions:
        if m.get("game_type") not in ("tvt1", "tvt2"):
            continue

        mission = dict(m)
        mission["id"] = m.get("id") or str(m.get("_id"))

        # Добавляем players_count (если в базе нет, то 0)
        mission["players_count"] = m.get("players_count", 0)

        result.append(mission)

    # Пагинация
    start = (page - 1) * per_page
    end = start + per_page
    paginated_result = result[start:end]

    return {
        "page": page,
        "per_page": per_page,
        "total": len(result),
        "total_pages": (len(result) + per_page - 1) // per_page if per_page else 1,
        "missions": paginated_result
    }
