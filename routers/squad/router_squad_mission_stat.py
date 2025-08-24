from fastapi import APIRouter, Query
from controllers.squad.controller_squad_mission_stat import controller_squad_stats

router = APIRouter()

@router.get("/squad-mission-stat")
def get_squad_mission_stat(file: str = Query(..., description="file")):
    return controller_squad_stats(file)
