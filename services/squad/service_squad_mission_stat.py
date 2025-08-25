from fastapi import HTTPException
from bd.bd import get_squads_by_file

def get_squad_statistics(file: str):
    try:
        squads = get_squads_by_file(file)

        result = []
        for squad in squads:
            victims = squad.get("victims_players", [])

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

            result.append(s)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")
