from fastapi import APIRouter, Query
from controllers.squad.controller_squad_top import controller_squad_top

router = APIRouter()

@router.get("/squad_top")
def get_squad_top(id: int = Query(..., description="id")):
    return controller_squad_top(id)
