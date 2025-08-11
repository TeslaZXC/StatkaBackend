from fastapi import APIRouter, Query
from controllers.controller_squad_top import controller_squad_top

router = APIRouter()

@router.get("/squad_top")
def get_squad_top(file_name: str = Query(..., description="Название файла, например stats_2025-05-01_2025-06-01.json")):
    return controller_squad_top(file_name)
