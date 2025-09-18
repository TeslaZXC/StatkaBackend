from fastapi import APIRouter
from controllers.mission.controller_mission_filtr import controller_mission_filtr

router = APIRouter()

@router.get("/mission-filter")
def router_mission_filtr():
    return controller_mission_filtr()
