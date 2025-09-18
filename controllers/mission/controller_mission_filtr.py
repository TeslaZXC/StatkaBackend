from services.mission.service_mission_filtr import get_mission_filtr

def controller_mission_filtr():
    return {"mission_name": get_mission_filtr()}
