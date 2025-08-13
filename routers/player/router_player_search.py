from fastapi import APIRouter, Query
from controllers.player.controller_player_search import get_player_search

router = APIRouter()

@router.get("/player-search")
def player_search_route(
    file_name: str = Query(..., description="Название блядства"),
    player_name: str = Query(..., description="Имя дауна поиск совпад ззз егойды")
):
    return get_player_search(file_name, player_name)
