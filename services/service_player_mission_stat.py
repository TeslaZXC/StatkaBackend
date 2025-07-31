import requests
from bs4 import BeautifulSoup
import re


def extract_unit_from_name(name: str) -> str:
    match = re.search(r"\[([^\[\]]+)\]", name)
    if match:
        return match.group(1)
    match = re.match(r"^([A-Za-z0-9]+)[\.\|\-_ ]", name)
    if match:
        return match.group(1)
    return ""


def parse_kill_or_death_row(row):
    cols = row.find_all("td")
    if len(cols) < 5:
        return None
    time = cols[1].get_text(strip=True)
    target = cols[2].get_text(strip=True)
    distance = cols[3].get_text(strip=True)
    weapon = cols[4].get_text(strip=True)
    return {
        "time": time,
        "target": target,
        "distance": distance,
        "weapon": weapon
    }


def parse_kill_death_details(player_td):
    details_div = player_td.find("div", class_="collapse")
    if not details_div:
        return [], None

    table = details_div.find("table")
    if not table:
        return [], None

    kills = []
    death = None

    mode = None
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 1:
            header = cols[0].get_text(strip=True).lower()
            if "kills" in header:
                mode = "kills"
            elif "death" in header:
                mode = "death"
        elif len(cols) >= 5:
            info = parse_kill_or_death_row(row)
            if not info:
                continue
            if mode == "kills":
                kills.append(info)
            elif mode == "death":
                death = info

    return kills, death


def get_player_mission_stats(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Не удалось получить страницу статистики")

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"id": "stats-table"})
    if not table:
        raise Exception("Таблица статистики не найдена")

    players = []

    for row in table.select("tbody tr"):
        cols = row.find_all("td")
        if len(cols) < 8:
            continue

        name = cols[0].get_text(strip=True)
        frags = int(cols[1].get_text(strip=True))
        side = cols[2].get_text(strip=True)
        group = cols[3].get_text(strip=True)
        deaths_text = cols[6].get_text(strip=True)
        deaths = int(deaths_text) if deaths_text.isdigit() else 0

        unit = extract_unit_from_name(name) or group

        kill_details, death_detail = parse_kill_death_details(cols[7])

        players.append({
            "name": name,
            "squad": unit,
            "side": side,
            "group": group,
            "frags": frags,
            "kills_detailed": kill_details,
            "death_detailed": death_detail
        })

    return {"players": players}
