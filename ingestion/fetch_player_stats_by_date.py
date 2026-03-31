import requests
import time
import json
from pathlib import Path

data_types = [
    "basicStats",
    "faceOffStats",
    "passes",
    "shotStats",
    "goalStats",
    "powerplayPenaltykillStats",
    "penaltyStats",
    "gameTime",
    "skatingStats",
    "advancedStats",
]

tournament = "playoffs"
season = "2025"

dates_file = f"data/raw/schedule_dates/{tournament}_{season}_dates.txt"

output_dir = Path(f"data/raw/player_stats/{tournament}_{season}")
output_dir.mkdir(parents=True, exist_ok=True)

base_url = "https://liiga.fi/api/v2/players/stats/summed"

with open(dates_file) as f:
    dates = [line.strip() for line in f]

for d in dates:
    day_data = {
        "date": d,
        "tournament": tournament,
        "data": {}
    }

    for dt in data_types:
        url = f"{base_url}/{d}/{d}/{tournament}/false"
        params = {
            "dataType": dt
        }

        r = requests.get(url, params=params)
        r.raise_for_status()

        day_data["data"][dt] = r.json()

        time.sleep(2)

    filename = output_dir / f"{d}.json"

    with open(filename, "w") as f:
        json.dump(day_data, f)

    print(f"Saved: {filename}")