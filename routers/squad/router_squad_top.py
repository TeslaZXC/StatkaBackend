from fastapi import APIRouter, Query
from controllers.squad.controller_squad_top import controller_squad_top

router = APIRouter()

@router.get("/squad_top")
def get_squad_top(file_name: str = Query(..., description="Название блядства")):
    return controller_squad_top(file_name)
