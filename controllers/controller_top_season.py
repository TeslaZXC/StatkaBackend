from services.service_top_season import get_top_season

def controller_top_season(file_name: str):
    return get_top_season(file_name)
