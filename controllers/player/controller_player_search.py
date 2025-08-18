from services.player.service_player_search import search_player_names

def get_player_search(id: int, player_name: str):
    return search_player_names(id, player_name)
