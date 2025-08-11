from fastapi import APIRouter, Query
from controllers.controller_squad_stat import controller_squad_stat

router = APIRouter()

@router.get("/squad-stat")
def get_squad_by_tag(
    file_name: str = Query(..., description="Название файла, например stats_2025-05-01_2025-06-01.json"),
    tag: str = Query(..., description="Тег сквада")
):
    return controller_squad_stat(file_name, tag)
