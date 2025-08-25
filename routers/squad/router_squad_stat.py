from fastapi import APIRouter, Query
from controllers.squad.controller_squad_stat import controller_squad_stat

router = APIRouter()

@router.get("/squad-stat")
def get_squad_by_tag_period(
    squad_tag: str = Query(..., description="Тег сквада"),
    start_date: str = Query(..., description="Начальная дата периода, YYYY-MM-DD"),
    end_date: str = Query(..., description="Конечная дата периода, YYYY-MM-DD")
):
    return controller_squad_stat(squad_tag, start_date, end_date)
