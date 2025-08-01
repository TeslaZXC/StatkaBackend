from services import service_player_search

def get_player_search(player_name: str):
    return service_player_search.search_player_names(player_name)
