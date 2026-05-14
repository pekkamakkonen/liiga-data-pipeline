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

        r = requests.get(url, params=params)
        r.raise_for_status()

        day_data["data"][dt] = r.json()

        time.sleep(2)

    filename = output_dir / f"{d}.json"

    with open(filename, "w") as f:
        json.dump(day_data, f)

    print(f"Saved: {filename}")