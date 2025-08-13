from fastapi import APIRouter, Query
from controllers.controller_top_season import controller_top_season

router = APIRouter()

@router.get("/top-season")
def top_season_route(
    file_name: str = Query(..., description="Название блядства")
):
    return controller_top_season(file_name)
