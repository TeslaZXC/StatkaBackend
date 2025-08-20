import os
import re
from fastapi import HTTPException
from services.config import TEMP_DIR

def get_season():
    try:
        if not os.path.exists(TEMP_DIR):
            raise HTTPException(status_code=404, detail="Папка temp не найдена.")

        files = os.listdir(TEMP_DIR)
        pattern = re.compile(r"^stats_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})\.json$")

        seasons = []

        seasons.append({
            "season_number": 0,
            "file_name": "all_stats.json",  
            "start_date": "-",  
            "end_date": "-"     
        })

        season_number = 1
        for filename in sorted(files):
            match = pattern.match(filename)
            if match:
                start_date, end_date = match.groups()
                seasons.append({
                    "season_number": season_number,
                    "file_name": filename,
                    "start_date": start_date,
                    "end_date": end_date
                })
                season_number += 1

        return seasons

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении списка сезонов: {str(e)}")
