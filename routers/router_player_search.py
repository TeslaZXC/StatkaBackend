from fastapi import APIRouter, Query
from controllers.controller_player_search import get_player_search

router = APIRouter()

@router.get("/player-search")
def player_search_route(
    file_name: str = Query(..., description="Название файла, например stats_2025-05-01_2025-06-01.json"),
    player_name: str = Query(..., description="Имя игрока для поиска (частичное совпадение)")
):
    return get_player_search(file_name, player_name)
