import requests
from bs4 import BeautifulSoup
import re
import json
from collections import defaultdict
import os


def extract_unit_from_name(name: str) -> str:
    match = re.search(r"\[([^\[\]]+)\]", name)
    if match:
        return match.group(1).upper()
    match = re.match(r"^([A-Za-z0-9]+)[\.\|\-_ ]", name)
    if match:
        return match.group(1).upper()
    return ""


def parse_kill_or_death_row(row):
    cols = row.find_all("td")
    if len(cols) < 5:
        return None
    return {
        "time": cols[1].get_text(strip=True),
        "target": cols[2].get_text(strip=True),
        "distance": cols[3].get_text(strip=True),
        "weapon": cols[4].get_text(strip=True),
    }


def parse_kill_death_details(player_td):
    details_div = player_td.find("div", class_="collapse")
    if not details_div:
        return [], None

    table = details_div.find("table")
    if not table:
        return [], None

    kills, death = [], None
    mode = None

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 1:
            header = cols[0].get_text(strip=True).lower()
            mode = "kills" if "kills" in header else "death" if "death" in header else None
        elif len(cols) >= 5 and mode:
            info = parse_kill_or_death_row(row)
            if info:
                if mode == "kills":
                    kills.append(info)
                elif mode == "death":
                    death = info

    return kills, death


def get_team_tags():
    filepath = os.path.join("data", "team.json")
    with open(filepath, "r", encoding="utf-8") as f:
        teams = json.load(f)
    return set(tag.upper() for tag in teams.keys())


def get_squad_statistics(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Не удалось получить страницу статистики")

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"id": "stats-table"})
    if not table:
        raise Exception("Таблица статистики не найдена")

    team_tags = get_team_tags()

    squad_data = defaultdict(lambda: {"side": None, "frags": 0, "deaths": 0, "players": 0})

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

        squad_tag = extract_unit_from_name(name)

        if squad_tag not in team_tags:
            continue

        _, death_detail = parse_kill_death_details(cols[7])
        actual_death_count = 1 if death_detail else 0

        squad = squad_data[squad_tag]
        if squad["side"] is None:
            squad["side"] = side
        elif squad["side"] != side:
            squad["invalid"] = True

        squad["frags"] += frags
        squad["deaths"] += actual_death_count
        squad["players"] += 1

    result = []
    for tag, stats in squad_data.items():
        if not stats.get("invalid"):
            result.append({
                "squad": tag,
                "side": stats["side"],
                "frags": stats["frags"],
                "deaths": stats["deaths"],
                "players": stats["players"]
            })

    return result
