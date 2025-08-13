from services.player.service_player_stat import load_player_by_name

def get_player_by_name(id: int, player_name: str):
    return load_player_by_name(id, player_name)
