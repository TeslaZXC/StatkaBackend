from fastapi import APIRouter, Query
from controllers.controller_team_players import controller_team_players

router = APIRouter()

@router.get("/team-players")
def team_players_route(
    id: int = Query(..., description="id блядства"),
    tag: str = Query(..., description="Тег отряда")
):
    return controller_team_players(id, tag)
