from fastapi import APIRouter, Query
from controllers.controller_squad_mission_stat import controller_squad_stats

router = APIRouter()

@router.get("/squad-mission-stat")
def get_squad_mission_stat(url: str = Query(..., description="url")):
    return controller_squad_stats(url)
