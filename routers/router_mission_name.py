from fastapi import APIRouter
from controllers.controller_mission_name import get_mission_name

router = APIRouter()

@router.get("/mission-name/{mission_id}")
def router_mission_name(mission_id: int):
    return get_mission_name(mission_id)
