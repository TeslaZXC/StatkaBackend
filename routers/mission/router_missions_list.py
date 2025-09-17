from fastapi import APIRouter
from controllers.mission.controller_missions_list import fetch_mission_list

router = APIRouter()

@router.get("/mission-list")
def mission_list(
    game_type: str = None,
    win_side: str = None,
    world_name: str = None,
    mission_name: str = None,
    file_date: str = None,
    page : int = None,
    per_page : int = None
):
    return fetch_mission_list(
        game_type=game_type,
        win_side=win_side,
        world_name=world_name,
        mission_name=mission_name,
        file_date=file_date,
        page = page,
        per_page= per_page
    )
