from services.player.service_player_search import search_player_names

def get_player_search(query: str, start_date: str, end_date: str):
    return search_player_names(query, start_date, end_date)
