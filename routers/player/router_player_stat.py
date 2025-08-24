from fastapi import APIRouter, Query
from controllers.player.controller_player_stat import get_player_stats_by_date

router = APIRouter()

@router.get("/player-stat")
def player_stat(
    player_name: str = Query(..., description="Имя игрока"),
    start_date: str = Query(..., description="Начальная дата (формат YYYY_MM_DD)"),
    end_date: str = Query(..., description="Конечная дата (формат YYYY_MM_DD)")
):
    """
    Собирает статистику игрока за указанный период времени (по file_date).
    """
    return get_player_stats_by_date(player_name, start_date, end_date)
