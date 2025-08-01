from fastapi import APIRouter
from controllers.controller_player_search import get_player_search

router = APIRouter()

@router.get("/player-search/{player_name}")
def player_search_route(player_name: str):
    return get_player_search(player_name)