from fastapi import APIRouter, Query
from controllers.controller_player_stat import get_player_by_name

router = APIRouter()

@router.get("/player-stat")
def get_player(
    file_name: str = Query(..., description="Название файла, например stats_2025-05-01_2025-06-01.json"),
    player_name: str = Query(..., description="Имя игрока для поиска")
):
    return get_player_by_name(file_name, player_name)
