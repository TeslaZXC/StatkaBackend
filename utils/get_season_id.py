import os
import re
from services.config import TEMP_DIR 

def get_season_file_by_id(season_id: int) -> str:
    if not os.path.exists(TEMP_DIR):
        raise FileNotFoundError("Папка temp не найдена.")

    files = os.listdir(TEMP_DIR)
    pattern = re.compile(r"^stats_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})\.json$")

    seasons = []
    season_number = 1

    for filename in sorted(files):
        match = pattern.match(filename)
        if match:
            seasons.append({
                "season_number": season_number,
                "file_name": filename
            })
            season_number += 1

    if not seasons:
        raise FileNotFoundError("Файлы сезонов не найдены.")

    for season in seasons:
        if season["season_number"] == season_id:
            return season["file_name"]

    raise ValueError(f"Сезон с ID {season_id} не найден.")
