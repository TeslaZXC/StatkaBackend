from fastapi import APIRouter, Query
from controllers.squad.controller_squad_stat import controller_squad_stat

router = APIRouter()

@router.get("/squad-stat")
def get_squad_by_tag(
    id: int = Query(..., description="Название блядства"),
    tag: str = Query(..., description="Тег сквада")
):
    return controller_squad_stat(id, tag)
