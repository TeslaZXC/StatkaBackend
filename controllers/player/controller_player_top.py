from services.player.service_player_top import get_top_inf_player,get_top_veh_player,get_top_all_player

def get_top_inf_players(id : int):
    return get_top_inf_player(id)

def get_top_veh_players(id : int):
    return get_top_veh_player(id)

def get_top_all_players(id : int):
    return get_top_all_player(id)