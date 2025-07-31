import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os
import re
import time

TEAM_JSON = "data/team.json"

PLAYERS_JSON = "data/players.json"
SQUADS_JSON = "data/squads.json"
BASE_URL = "https://stats.red-bear.ru"
OCAP_URL = "https://ocap.red-bear.ru"

MONTHS_TO_PARSE = 3

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

def get_mission_list():
    url = "https://stats.red-bear.ru/"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    table = soup.find("table", {"id": "ocap-list-table"})
    if not table:
        print("ocap-list-table не найден")
        return []

    rows = table.find("tbody").find_all("tr")
    missions = []
    cutoff = datetime.now() - timedelta(days=30 * MONTHS_TO_PARSE)

    for row in rows:
        tds = row.find_all("td")
        if len(tds) <= 9:
            continue

        date_str = tds[9].get_text(strip=True)
        try:
            mission_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                mission_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print(f"Нераспознан формат даты: {date_str}")
                continue

        if mission_date >= cutoff:
            link = row.find("a", class_="replay_id link")
            if not link or not link.get("href"):
                continue

            href = link.get("href")
            if "mission_tag=tvt" not in href:
                continue

            missions.append({
                "url": "https://stats.red-bear.ru" + href,
                "date": mission_date.strftime("%Y-%m-%d %H:%M")
            })

    print(f"Найдено подходящих миссий с tag=tvt: {len(missions)}")
    return missions


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_player_stats(url, team_tags):
    print(f"[>] Парсинг {url}")
    for attempt in range(2):
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                continue

            soup = BeautifulSoup(resp.text, "lxml")
            table = soup.find("table", {"id": "stats-table"})
            if not table:
                continue

            players = []
            squads = defaultdict(lambda: {"frags": 0, "deaths": 0, "side": None, "players": 0})

            rows = table.select("tbody tr")
            if not rows and attempt == 0:
                print("Игроков не найдено. Повторная попытка...")
                time.sleep(1)
                continue

            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 8:
                    continue

                name = cols[0].get_text(strip=True)
                frags = int(cols[1].get_text(strip=True))
                side = cols[2].get_text(strip=True)
                group = cols[3].get_text(strip=True)
                deaths_text = cols[6].get_text(strip=True)
                deaths = int(deaths_text) if deaths_text.isdigit() else 0

                kills_detailed, death_detailed = parse_kill_death_details(cols[7])
                death = 1 if death_detailed else 0

                squad_tag = extract_unit_from_name(name)

                players.append({
                    "name": name,
                    "squad": extract_unit_from_name(name),
                    "side": side,
                    "group": group,
                    "frags": frags,
                    "deaths": death,
                    "kills_detailed": kills_detailed,
                    "death_detailed": [death_detailed] if death_detailed else []
                })

                if squad_tag in team_tags:
                    s = squads[squad_tag]
                    s["frags"] += frags
                    s["deaths"] += death
                    s["players"] += 1
                    if s["side"] is None:
                        s["side"] = side
                    elif s["side"] != side:
                        s["side"] = "mixed"

            return players, squads
        except Exception as e:
            print("Ошибка:", e)
    return [], {}

def clean_name(name: str) -> str:
    name = re.sub(r"\[[^\[\]]+\]\s*", "", name)
    name = re.sub(r"^[A-Za-z0-9]+[\.\|\-_ ]+", "", name)
    return name.strip()


def update_stats():
    team_tags = set(load_json_file(TEAM_JSON).keys())
    player_stats = load_json_file(PLAYERS_JSON)
    squad_stats = load_json_file(SQUADS_JSON)

    missions = get_mission_list()
    for mission in missions:
        url = mission["url"]
        date = mission["date"]

        players, squads = parse_player_stats(url, team_tags)

        for p in players:
            name = clean_name(p["name"])
            frags_real = max(p["frags"], len(p["kills_detailed"]))
            deaths_real = max(p["deaths"], len(p["death_detailed"]))
            squad_tag = extract_unit_from_name(p["name"])

            if name not in player_stats:
                player_stats[name] = {
                    "name": name,
                    "squad": squad_tag,
                    "squad_history": [squad_tag] if squad_tag else [],
                    "side": p["side"],
                    "group": p["group"],
                    "frags": frags_real,
                    "deaths": deaths_real,
                    "kills_detailed": p["kills_detailed"],
                    "death_detailed": p["death_detailed"],
                    "missions": [url]
                }
            else:
                ps = player_stats[name]
                if url in ps.get("missions", []):
                    continue

                if squad_tag and squad_tag != ps.get("squad"):
                    ps["squad"] = squad_tag
                    if squad_tag not in ps["squad_history"]:
                        ps["squad_history"].append(squad_tag)

                ps["frags"] += frags_real
                ps["deaths"] += deaths_real
                ps["kills_detailed"].extend(p["kills_detailed"])
                ps["death_detailed"].extend(p["death_detailed"])
                ps["missions"].append(url)

        squad_members = defaultdict(set)
        for p in players:
            tag = extract_unit_from_name(p["name"])
            if tag:
                squad_members[tag].add(clean_name(p["name"]))

        for tag, stats in squads.items():
            if tag not in squad_stats:
                squad_stats[tag] = {
                    "frags": stats["frags"],
                    "deaths": stats["deaths"],
                    "players": stats["players"],
                    "side": stats["side"],
                    "members": list(squad_members[tag]),
                    "missions": 1,
                    "total_attendance": stats["players"]
                }
            else:
                ss = squad_stats[tag]
                ss["frags"] += stats["frags"]
                ss["deaths"] += stats["deaths"]
                ss["players"] += stats["players"]
                ss["missions"] = ss.get("missions", 0) + 1
                ss["total_attendance"] = ss.get("total_attendance", 0) + stats["players"]
                existing_members = set(ss.get("members", []))
                new_members = squad_members[tag]
                ss["members"] = list(existing_members.union(new_members))

    for tag, ss in squad_stats.items():
        missions = ss.get("missions", 0)
        total_attendance = ss.get("total_attendance", 0)
        if missions > 0:
            ss["average_attendance"] = round(total_attendance / missions, 2)
        else:
            ss["average_attendance"] = 0.0

    for tag, ss in squad_stats.items():
        missions = ss.get("missions", 0)
        average_attendance = ss.get("average_attendance", 0)
        frags = ss.get("frags", 0)

        if missions > 0 and average_attendance > 0:
            ss["score"] = round((frags / missions) / average_attendance, 4)
        else:
            ss["score"] = 0.0

    print("Сохраняю результаты...")
    save_json_file(PLAYERS_JSON, player_stats)
    save_json_file(SQUADS_JSON, squad_stats)
    print("Готово.")


if __name__ == "__main__":
    update_stats()