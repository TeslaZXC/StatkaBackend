from fastapi import APIRouter, Query
from controllers.player.controller_player_search import get_player_search

router = APIRouter()

@router.get("/player-search")
def player_search_route(
    id: int = Query(..., description="id блядства"),
    player_name: str = Query(..., description="Имя дауна поиск совпад ззз егойды")
):
    return get_player_search(id, player_name)
