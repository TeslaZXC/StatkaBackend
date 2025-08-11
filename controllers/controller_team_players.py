from services.service_team_players import get_team_players

def controller_team_players(file_name: str, tag: str):
    return get_team_players(file_name, tag)
