import uuid
from fastapi import HTTPException, Request
from bd.bd import save_ocap_token, get_ocap_token, find_ocap_token_by_ip_and_data


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
    try:
        user_ip = request.client.host 

        data = {
            "urlOcap": urlOcap,
            "missionName": missionName,
            "killName": killName,
            "killerName": killerName,
            "timeKill": timeKill,
            "weapon": weapon,
            "distance": distance,
            "idMission": idMission
        }

        existing = find_ocap_token_by_ip_and_data(user_ip, data)
        if existing:
            return {"short_link": f"/api/ocap/share/{existing['short_id']}"}

        short_id = str(uuid.uuid4())[:8]  
        payload = {
            "short_id": short_id,
            "user_ip": user_ip,
            **data
        }

        save_ocap_token(payload)

        return {"short_link": f"/api/ocap/share/{short_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации ссылки: {str(e)}")


def decode_ocap_token(short_id: str):
    try:
        doc = get_ocap_token(short_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при расшифровке ссылки: {str(e)}")
