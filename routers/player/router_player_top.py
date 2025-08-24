from fastapi import APIRouter, Query
from controllers.player.controller_player_top import get_top_all_players, get_top_inf_players, get_top_veh_players

router = APIRouter()

@router.get("/player-top", description="Топ по всем фрагам")
def get_top_players_route(
    start_date: str = Query(..., description="Дата начала в формате YYYY-MM-DD"),
    end_date: str = Query(..., description="Дата конца в формате YYYY-MM-DD")
):
    return get_top_all_players(start_date, end_date)

@router.get("/player-top-inf", description="Топ по фрагам пехоты")
def get_top_inf_players_route(
    start_date: str = Query(..., description="Дата начала в формате YYYY-MM-DD"),
    end_date: str = Query(..., description="Дата конца в формате YYYY-MM-DD")
):
    return get_top_inf_players(start_date, end_date)

@router.get("/player-top-veh", description="Топ по фрагам техники")
def get_top_veh_players_route(
    start_date: str = Query(..., description="Дата начала в формате YYYY-MM-DD"),
    end_date: str = Query(..., description="Дата конца в формате YYYY-MM-DD")
):
    return get_top_veh_players(start_date, end_date)
