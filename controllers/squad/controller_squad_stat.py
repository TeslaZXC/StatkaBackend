from fastapi import HTTPException
from services.squad.service_squad_stat import get_squad_stat

def controller_squad_stat(id: int, tag: str):
    squad_data = get_squad_stat(id, tag)
    if not squad_data:
        raise HTTPException(status_code=404, detail=f"Squad '{tag}' not found")
    return squad_data
