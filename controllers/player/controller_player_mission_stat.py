from services.player.service_player_mission_stat import get_player_mission_stats

def get_player_mission_stats_controller(mission_id: int):
    return get_player_mission_stats(mission_id)
