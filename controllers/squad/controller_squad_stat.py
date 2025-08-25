from fastapi import HTTPException
from services.squad.service_squad_stat import get_squad_stat_by_period

def controller_squad_stat(squad_tag: str, start_date: str, end_date: str):
    return get_squad_stat_by_period(squad_tag, start_date, end_date)
