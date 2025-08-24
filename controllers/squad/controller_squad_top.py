from services.squad.service_squad_top import get_squad_top_by_period

def controller_squad_top_period(start_date: str, end_date: str):
    return get_squad_top_by_period(start_date, end_date)
