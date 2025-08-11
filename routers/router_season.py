from fastapi import APIRouter
from controllers.controller_season import get_season

router = APIRouter()

@router.get("/season")
def fetch_season():
    return get_season()
