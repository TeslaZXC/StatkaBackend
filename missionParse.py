import requests
from bs4 import BeautifulSoup
import os
import re
import json
from collections import defaultdict

DIR_BASE = "data/mission"
DIR_STAT = os.path.join(DIR_BASE, "stat")
DIR_PLAYER = os.path.join(DIR_BASE, "player")
DIR_SQUAD = os.path.join(DIR_BASE, "squad")
TEAM_FILE = "data/team.json"

os.makedirs(DIR_STAT, exist_ok=True)
os.makedirs(DIR_PLAYER, exist_ok=True)
os.makedirs(DIR_SQUAD, exist_ok=True)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

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
    with open(TEAM_FILE, "r", encoding="utf-8") as f:
        teams = json.load(f)
    return set(tag.upper() for tag in teams.keys())

BASE_URL = "https://stats.red-bear.ru"
OCAP_URL = "https://ocap.red-bear.ru"

def get_mission_list(limit=100):
    url = f"{BASE_URL}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "ocap-list-table"})
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    missions = []

    i = 0
    while i < len(rows):
        try:
            title_row = rows[i]
            tds = title_row.find_all("td")
            title_link = title_row.find("a", class_="replay_id link")

            if i + 1 < len(rows):
                play_row = rows[i + 1]
                play_link_tag = play_row.find("a", class_="cell-link")
                play_href = play_link_tag.get("href") if play_link_tag else None
                play_link_full = play_href if play_href and play_href.startswith("http") else f"{OCAP_URL}{play_href}" if play_href else None
            else:
                play_link_full = None

            if not title_link:
                i += 2
                continue

            mission_name = title_link.text.strip()
            json_href = title_link.get("href")
            json_link = f"{BASE_URL}{json_href}"

            values = [td.get_text(strip=True) for td in tds]

            # Фильтрация по mission_tag
            if "mission_tag=" in json_href:
                mission_tag_match = re.search(r"mission_tag=([a-zA-Z0-9_]+)", json_href)
                mission_tag = mission_tag_match.group(1) if mission_tag_match else None
                if mission_tag != "tvt":
                    i += 2
                    continue
            else:
                i += 2
                continue

            mission_data = {
                "id": int(values[0]) if len(values) > 0 else None,
                "mission_name": mission_name,
                "json_link": json_link,
                "play_link": play_link_full,
                "total_players": values[3] if len(values) > 3 else None,
                "map": values[7] if len(values) > 7 else None,
                "duration": values[8] if len(values) > 8 else None,
                "date": values[9] if len(values) > 9 else None,
            }

            if mission_data["id"] is not None:
                missions.append(mission_data)

        except Exception:
            pass

        i += 2

    missions.sort(key=lambda x: x["id"], reverse=True)
    return missions[:limit]

def get_player_stats(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    table = soup.find("table", {"id": "stats-table"})
    if not table:
        return {"players": []}

    players = []
    for row in table.select("tbody tr"):
        cols = row.find_all("td")
        if len(cols) < 8:
            continue

        name = cols[0].get_text(strip=True)
        frags = int(cols[1].get_text(strip=True))
        side = cols[2].get_text(strip=True)
        group = cols[3].get_text(strip=True)
        teamkills = int(cols[4].get_text(strip=True) or 0)
        vehicle_kills = int(cols[5].get_text(strip=True) or 0)
        deaths = int(cols[6].get_text(strip=True) or 0)

        unit = extract_unit_from_name(name) or group
        kill_details, death_detail = parse_kill_death_details(cols[7])

        players.append({
            "name": name,
            "squad": unit,
            "side": side,
            "group": group,
            "frags": frags,
            "teamkills": teamkills,
            "vehicle_kills": vehicle_kills,
            "kills_detailed": kill_details,
            "death_detailed": death_detail
        })

    return {"players": players}

def get_squad_stats(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    table = soup.find("table", {"id": "stats-table"})
    if not table:
        return []

    team_tags = get_team_tags()
    squad_data = defaultdict(lambda: {"side": None, "frags": 0, "deaths": 0, "players": 0})

    for row in table.select("tbody tr"):
        cols = row.find_all("td")
        if len(cols) < 8:
            continue

        name = cols[0].get_text(strip=True)
        frags = int(cols[1].get_text(strip=True))
        side = cols[2].get_text(strip=True)
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

def mission_file_exists(mission_id):
    # Проверим, есть ли все три файла
    stat = os.path.exists(os.path.join(DIR_STAT, f"{mission_id}.json"))
    player = os.path.exists(os.path.join(DIR_PLAYER, f"{mission_id}.json"))
    squad = os.path.exists(os.path.join(DIR_SQUAD, f"{mission_id}.json"))
    return stat and player and squad

def main():
    missions = get_mission_list(limit=100)

    for mission in missions:
        mission_id = mission["id"]

        if mission_file_exists(mission_id):
            print(f"[✓] Миссия {mission_id} уже скачана. Пропускаем.")
            continue

        print(f"[+] Скачиваем миссию {mission_id}: {mission['mission_name']}")

        try:
            save_json(os.path.join(DIR_STAT, f"{mission_id}.json"), mission)

            player_stats = get_player_stats(mission["json_link"])
            save_json(os.path.join(DIR_PLAYER, f"{mission_id}.json"), player_stats)

            squad_stats = get_squad_stats(mission["json_link"])
            save_json(os.path.join(DIR_SQUAD, f"{mission_id}.json"), squad_stats)

        except Exception as e:
            print(f"[!] Ошибка при обработке миссии {mission_id}: {e}")


if __name__ == "__main__":
    main()
