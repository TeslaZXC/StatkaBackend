from fastapi import APIRouter
from controllers.mission.controller_missions_list import get_mission_list

router = APIRouter()

@router.get("/mission-list")
def fetch_at_mission():
    return get_mission_list()
