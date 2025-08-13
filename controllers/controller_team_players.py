from services.service_team_players import get_team_players

def controller_team_players(id: int, tag: str):
    return get_team_players(id, tag)
