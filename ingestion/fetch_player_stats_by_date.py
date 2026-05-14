import requests
import time
import json
from pathlib import Path
from datetime import datetime, timezone

data_types = [
    "basicStats",
    "faceOffStats",
    "passes",
    "shotStats",
    "goalStats",
    "winningShotComp",
    "powerplayPenaltykillStats",
    "penaltyStats",
    "gameTime",
    "skatingStats",
    "advancedStats",
    "basicStatsGk",
    "winningShotCompGk"   
]

tournament = "runkosarja"
season = "2026"

dates_file = f"data/raw/schedule_dates/{tournament}_{season}_dates.txt"

output_dir = Path(f"data/raw/player_stats/{tournament}_{season}")
output_dir.mkdir(parents=True, exist_ok=True)

base_url = "https://liiga.fi/api/v2/players/stats/summed"

with open(dates_file) as f:
    dates = [line.strip() for line in f]

for d in dates:
    day_data = {
        "season": int(season),
        "tournament": tournament,
        "game_date": d,
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "data": {}
    }

    for dt in data_types:
        url = f"{base_url}/{d}/{d}/{tournament}/false"
        params = {
            "dataType": dt
        }

        max_retries = 3

        for attempt in range(max_retries):
            try:
                r = requests.get(url, params=params)
                r.raise_for_status()

                response_json = r.json()
                break

            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed for {url}")
                print(e)

                time.sleep(10)

        else:
            raise Exception(f"Failed after {max_retries} attempts: {url}")

        day_data["data"][dt] = response_json

        time.sleep(2)

    filename = output_dir / f"{d}.json"

    with open(filename, "w") as f:
        json.dump(day_data, f)

    print(f"Saved: {filename}")