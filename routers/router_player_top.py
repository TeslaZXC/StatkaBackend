from fastapi import APIRouter, Query
from controllers.controller_player_top import get_top_players

router = APIRouter()

@router.get("/player-top")
def get_top_players_route(
    file_name: str = Query(..., description="Название файла, например stats_2025-05-01_2025-06-01.json")
):
    return get_top_players(file_name)
