from fastapi import APIRouter
from controllers.controller_find_mission import fetch_find_mission

router = APIRouter()

@router.get("/find-mission")
def find_mission_route(
    file: str,
    file_date: str
):
    return fetch_find_mission(file=file, file_date=file_date)
