from services.mission.service_mission_name import get_mission_info_by_id

def get_mission_name(mission_id: int):
    return {"mission_name": get_mission_info_by_id(mission_id)}
