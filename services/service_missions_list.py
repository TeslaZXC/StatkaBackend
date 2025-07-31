import requests
from bs4 import BeautifulSoup

def get_mission_list():
    url = "https://stats.red-bear.ru/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "ocap-list-table"})
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")
    missions = []

    for i in range(0, len(rows) - 1, 2):
        try:
            title_row = rows[i]
            play_row = rows[i + 1]

            tds = title_row.find_all("td")
            title_link = title_row.find("a", class_="replay_id link")
            play_link = play_row.find("a", class_="cell-link")

            if not title_link or not play_link:
                continue

            mission_name = title_link.text.strip()
            json_href = title_link.get("href")
            json_link = f"https://stats.red-bear.ru{json_href}"

            play_href = play_link.get("href")
            play_link_full = play_href if play_href.startswith("http") else f"https://ocap.red-bear.ru{play_href}"

            values = [td.get_text(strip=True) for td in tds]

            mission_data = {
                "id": values[0] if len(values) > 0 else None,
                "mission_name": mission_name,
                "json_link": json_link,
                "play_link": play_link_full,
                "total_players": values[3] if len(values) > 3 else None,
                "map": values[7] if len(values) > 7 else None,
                "duration": values[8] if len(values) > 8 else None,
                "date": values[9] if len(values) > 9 else None,
            }

            missions.append(mission_data)

        except Exception:
            continue

    return missions
