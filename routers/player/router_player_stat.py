from fastapi import APIRouter, Query
from controllers.player.controller_player_stat import get_player_by_name

router = APIRouter()

@router.get("/player-stat")
def get_player(
    id: int = Query(..., description= "id блядства"),
    player_name: str = Query(..., description="Имя дауна")
):
    return get_player_by_name(id, player_name)
