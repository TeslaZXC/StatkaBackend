from fastapi import APIRouter
from controllers import controller_player_top

router = APIRouter()

@router.get("/player-top")
def get_top_players():
    return controller_player_top.get_top_players()
