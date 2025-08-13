from fastapi import APIRouter, Query
from controllers.player.controller_player_stat import get_player_by_name

router = APIRouter()

@router.get("/player-stat")
def get_player(
    file_name: str = Query(..., description= "Название блядства"),
    player_name: str = Query(..., description="Имя дауна")
):
    return get_player_by_name(file_name, player_name)
