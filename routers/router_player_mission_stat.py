from fastapi import APIRouter, Query
from controllers.controller_player_mission_stat import get_player_mission_stats_controller

router = APIRouter()

@router.get("/player-mission-stats")
def get_player_mission_stats(mission_url: str = Query(..., description="url")):
    return get_player_mission_stats_controller(mission_url)
