from services.player.service_player_search import search_player_names

def get_player_search(file_name: str, player_name: str):
    return search_player_names(file_name, player_name)
