from services import servica_player_search

def get_player_search(player_name: str):
    return servica_player_search.search_player_names(player_name)
