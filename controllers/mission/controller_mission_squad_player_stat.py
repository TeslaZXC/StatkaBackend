from services.mission.service_mission_squad_player_stat import get_mission_squad_player_stat

def controller_mission_squad_player_stat(mission_id: int, squad_tag: str):
    return get_mission_squad_player_stat(mission_id, squad_tag)
