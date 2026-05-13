import requests
import time
import json
from pathlib import Path
from datetime import datetime, timezone

data_types = [
    "standings",
    "shots",
    "passes",
    "faceoffs",
    "even_strength",
    "powerplay",
    "penalty_kill",
    "penalties",
    "attendance"
]

tournament = "playoffs"
season = "2025"

dates_file = f"data/raw/schedule_dates/{tournament}_{season}_dates.txt"

output_dir = Path(f"data/raw/team_stats/{tournament}_{season}")
output_dir.mkdir(parents=True, exist_ok=True)

base_url = "https://liiga.fi/api/v2/teams/stats"

with open(dates_file) as f:
    dates = [line.strip() for line in f]

for d in dates:
    day_data = {
        "season": int(season),
        "tournament": tournament,
        "game_date": d,
        "fetched_at": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
        "data": {}
    }

    for dt in data_types:
        params = {
            "seasonFrom": d,
            "seasonTo": d,
            "tournament": tournament,
            "dataType": dt
        }

        r = requests.get(base_url, params=params)
        r.raise_for_status()

        day_data["data"][dt] = r.json()

        print(f"Fetched {dt} for {d}")

        time.sleep(2)

    filename = output_dir / f"{d}.json"

    with open(filename, "w") as f:
        json.dump(day_data, f)

    print(f"Saved: {filename}")