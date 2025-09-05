from fastapi import HTTPException
from bd.bd import get_squads_by_id, get_all_squads

def get_squad_statistics(id: int):
    try:
        squads = get_squads_by_id(id)
        if not squads:
            return []

        valid_squads_doc = get_all_squads()
        valid_squads = {str(k).strip().lower(): v for k, v in valid_squads_doc.items() if k != "_id"}

        result = []
        for squad in squads:
            tag = squad.get("squad_tag") or squad.get("tag")
            if not tag:
                continue  

            tag_lower = str(tag).strip().lower()

            if tag_lower not in valid_squads:
                continue  

            victims = squad.get("victims_players", []) or []

            frags_inf = 0
            frags_veh = 0
            teamkills = 0

            for v in victims:
                kt = str(v.get("kill_type", "")).lower()
                if kt == "tk":
                    teamkills += 1
                elif kt == "kill":
                    frags_inf += 1
                elif kt == "veh":
                    frags_veh += 1

            s = dict(squad)  
            s["stats"] = {
                "frags_inf": frags_inf,
                "frags_veh": frags_veh,
                "teamkills": teamkills
            }

            s["info"] = valid_squads[tag_lower]

            result.append(s)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")
