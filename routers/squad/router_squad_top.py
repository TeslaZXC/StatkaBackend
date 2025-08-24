from fastapi import APIRouter, Query
from controllers.squad.controller_squad_top import controller_squad_top_period
from typing import List, Dict

router = APIRouter()

@router.get("/squad_top_period", response_model=List[Dict])
def fetch_squad_top(
    start_date: str = Query(..., description="Дата начала в формате YYYY_MM_DD"),
    end_date: str = Query(..., description="Дата конца в формате YYYY_MM_DD")
):
    """
    Возвращает топ отрядов за указанный период.
    """
    return controller_squad_top_period(start_date, end_date)
