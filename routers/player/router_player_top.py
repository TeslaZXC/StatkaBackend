from fastapi import APIRouter, Query
from controllers.player.controller_player_top import get_top_players

router = APIRouter()

@router.get("/player-top")
def get_top_players_route(
    file_name: str = Query(..., description="Название блядства")
):
    return get_top_players(file_name)
