from fastapi import APIRouter
from controllers.controller_player_stat import get_player_by_name

router = APIRouter()

@router.get("/player-stat/{player_name}")
def get_player(player_name: str):
    return get_player_by_name(player_name)
