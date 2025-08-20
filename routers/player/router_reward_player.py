from fastapi import APIRouter, HTTPException
from controllers.player.controller_reward_player import get_json

router = APIRouter()

@router.get("/json")
def fetch_json(name: str):
    result = get_json(name)
    if result is None:
        raise HTTPException(status_code=404, detail="JSON with this name not found")
    return result