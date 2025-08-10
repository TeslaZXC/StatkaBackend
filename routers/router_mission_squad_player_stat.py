from fastapi import APIRouter, Query
from controllers.controller_mission_squad_player_stat import controller_mission_squad_player_stat

router = APIRouter()

@router.get("/mission_squad_player_stat")
def mission_squad_player_stat(
    mission_id: int = Query(..., description="ID миссии"),
    squad_tag: str = Query(..., description="Тег отряда без скобок")
):
    return controller_mission_squad_player_stat(mission_id, squad_tag)
