from fastapi import APIRouter, Query
from controllers.mission.controller_mission_squad_player_stat import controller_mission_squad_player_stat

router = APIRouter()

@router.get("/mission_squad_player_stat")
def mission_squad_player_stat(
    mission_id: int = Query(..., description="ID миски"),
    squad_tag: str = Query(..., description="отряд нейминг свага")
):
    return controller_mission_squad_player_stat(mission_id, squad_tag)
