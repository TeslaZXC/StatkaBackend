from services.player.service_player_stat import aggregate_player_stats_by_date

def get_player_stats_by_date(player_name: str, start_date: str, end_date: str):
    return aggregate_player_stats_by_date(player_name, start_date, end_date)
