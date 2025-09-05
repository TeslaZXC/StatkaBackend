from fastapi import APIRouter, Query
from controllers.player.controller_player_mission_stat import get_player_mission_stats_controller

router = APIRouter()

@router.get("/player-mission-stats")
def get_player_mission_stats(id: int = Query(..., description="id")):

    return get_player_mission_stats_controller(id)
