from services import service_player_stat

def get_player_by_name(player_name: str):
    return service_player_stat.load_player_by_name(player_name)
