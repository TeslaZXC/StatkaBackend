from fastapi import APIRouter, Query
from controllers.player.controller_player_search import get_player_search

router = APIRouter()

@router.get("/player-search")
def player_search_route(
    player_name: str = Query(..., description="Имя или его часть для поиска"),
    start_date: str = Query(..., description="Начальная дата (формат YYYY_MM_DD)"),
    end_date: str = Query(..., description="Конечная дата (формат YYYY_MM_DD)")
):
    return get_player_search(player_name, start_date, end_date)
