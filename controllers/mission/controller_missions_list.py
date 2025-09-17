from fastapi import Query
from typing import Optional
from services.mission.service_missions_list import get_mission_list

def fetch_mission_list(
    game_type: Optional[str] = Query(None),
    win_side: Optional[str] = Query(None),
    world_name: Optional[str] = Query(None),
    mission_name: Optional[str] = Query(None),
    file_date: Optional[str] = Query(None),
    page: Optional[int] = Query(None),
    per_page: Optional[int] = Query(None)
):
    return get_mission_list(
        game_type=game_type,
        win_side=win_side,
        world_name=world_name,
        mission_name=mission_name,
        file_date=file_date,
        page = page,
        per_page=per_page
    )
