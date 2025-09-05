import os
import json
from fastapi import HTTPException
from services.config import MISSION_DIR

from bd.bd import get_players_by_id

def get_player_mission_stats(id: int):
    try:
        data = get_players_by_id(id)
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")
