from fastapi import APIRouter, Query
from controllers.player.controller_player_mission_stat import get_player_mission_stats_controller

router = APIRouter()

@router.get("/player-mission-stats")
def get_player_mission_stats(file: str = Query(..., description="file")):
    return get_player_mission_stats_controller(file)
