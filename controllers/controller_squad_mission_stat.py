from services.service_squad_mission_stat import get_squad_statistics

def controller_squad_stats(url: str):
    return get_squad_statistics(url)