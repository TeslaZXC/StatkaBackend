from fastapi import Request
from services.service_ocap_token import generate_ocap_token as service_generate_ocap_token, decode_ocap_token as service_decode_ocap_token


async def generate_ocap_token(
    request: Request,
    urlOcap: str,
    missionName: str,
    killName: str,
    killerName: str,
    timeKill: str,
    weapon: str,
    distance: str,
    idMission: str
):
    return await service_generate_ocap_token(request, urlOcap, missionName, killName, killerName, timeKill, weapon, distance, idMission)


def decode_ocap_token(short_id: str):
    return service_decode_ocap_token(short_id)
