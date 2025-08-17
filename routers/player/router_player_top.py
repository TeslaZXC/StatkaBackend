from fastapi import APIRouter, Query
from controllers.player.controller_player_top import get_top_all_players,get_top_inf_players,get_top_veh_players

router = APIRouter()

@router.get("/player-top", description="топ по килам")
def get_top_players_route(
    id: int = Query(..., description="id блядства")
):
    return get_top_all_players(id)

@router.get("/player-top-veh", description="топ по тех")
def get_top_veh_players_route(
    id: int = Query(..., description="id блядства")
):
    return get_top_veh_players(id)

@router.get("/player-top-inf", description="топ по пех")
def get_top_inf_players_route(
    id: int = Query(..., description="id блядства")
):
    return get_top_inf_players(id)
