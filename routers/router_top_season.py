from fastapi import APIRouter, Query
from controllers.controller_top_season import controller_top_season

router = APIRouter()

@router.get("/top-season")
def top_season_route(
    file_name: str = Query(..., description="Название файла, например stats_2025-05-01_2025-06-01.json")
):
    return controller_top_season(file_name)
