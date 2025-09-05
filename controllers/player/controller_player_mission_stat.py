from services.player.service_player_mission_stat import get_player_mission_stats

def get_player_mission_stats_controller(id: int):
    return get_player_mission_stats(id)
