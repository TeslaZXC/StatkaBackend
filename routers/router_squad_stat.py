from fastapi import APIRouter
from controllers.controller_squad_stat import controller_squad_stat

router = APIRouter()

@router.get("/squad-stat/{tag}")
def get_squad_by_tag(tag: str):
    return controller_squad_stat(tag)
