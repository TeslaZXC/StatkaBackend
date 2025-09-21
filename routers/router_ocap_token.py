from fastapi import APIRouter, Request, Query
from controllers.controller_ocap_token import generate_ocap_token, decode_ocap_token

router = APIRouter()


@router.get("/ocap/generate-link")
async def fetch_generate_ocap_link(
    request: Request,
    urlOcap: str = Query(...),
    missionName: str = Query(...),
    killName: str = Query(...),
    killerName: str = Query(...),
    timeKill: str = Query(...),
    weapon: str = Query(...),
    distance: str = Query(...),
    idMission: str = Query(...)
):
    return await generate_ocap_token(request, urlOcap, missionName, killName, killerName, timeKill, weapon, distance, idMission)


@router.get("/ocap/share/{short_id}")
def fetch_decode_ocap_link(short_id: str):
    return decode_ocap_token(short_id)
