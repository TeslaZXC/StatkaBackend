from fastapi import APIRouter, Query
from controllers.controller_team_players import controller_team_players

router = APIRouter()

@router.get("/team-players")
def team_players_route(tag: str = Query(..., description="Тег отряда, например [UN] или Dw")):
    return controller_team_players(tag)
