from services.player.service_player_top import (
    get_top_all_players_by_period,
    get_top_inf_players_by_period,
    get_top_veh_players_by_period
)

def get_top_all_players(start_date: str, end_date: str):
    return get_top_all_players_by_period(start_date, end_date)

def get_top_inf_players(start_date: str, end_date: str):
    return get_top_inf_players_by_period(start_date, end_date)

def get_top_veh_players(start_date: str, end_date: str):
    return get_top_veh_players_by_period(start_date, end_date)
