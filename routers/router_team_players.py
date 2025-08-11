from fastapi import APIRouter, Query
from controllers.controller_team_players import controller_team_players

router = APIRouter()

@router.get("/team-players")
def team_players_route(
    file_name: str = Query(..., description="Название файла, например stats_2025-05-01_2025-06-01.json"),
    tag: str = Query(..., description="Тег отряда, например [UN] или Dw")
):
    return controller_team_players(file_name, tag)
