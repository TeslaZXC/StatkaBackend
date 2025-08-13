from services.player.service_player_stat import load_player_by_name

def get_player_by_name(file_name: str, player_name: str):
    return load_player_by_name(file_name, player_name)
