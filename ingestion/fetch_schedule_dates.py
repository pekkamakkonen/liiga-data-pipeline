import requests
import time
from pathlib import Path

configs = [
    ("runkosarja", 2023),
    ("runkosarja", 2024),
    ("runkosarja", 2025),
    ("runkosarja", 2026),
    ("playoffs", 2023),
    ("playoffs", 2024),
    ("playoffs", 2025),
    ("playoffs", 2026),
]

base_url = "https://www.liiga.fi/api/v2/schedule"

output_dir = Path("data/raw/schedule_dates")
output_dir.mkdir(parents=True, exist_ok=True)

for tournament, season in configs:
    params = {
        "tournament": tournament,
        "season": season
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    dates = sorted({
        item["start"][:10]
        for item in data
        if "start" in item
    })

    filename = output_dir / f"{tournament}_{season}_dates.txt"

    with open(filename, "w") as f:
        for d in dates:
            f.write(d + "\n")

    print(f"{tournament} {season}: {len(dates)} dates saved")

    time.sleep(2)  # ← ODOTUS (2 sekuntia per request)