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

output_dir = Path("data/raw/game_ids")
output_dir.mkdir(parents=True, exist_ok=True)

for tournament, season in configs:
    params = {
        "tournament": tournament,
        "season": season
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    game_ids = set()

    for item in data:
        if "games" in item:
            for game in item["games"]:
                game_ids.add(game["id"])
        elif "id" in item:
            game_ids.add(item["id"])

    game_ids = sorted(game_ids)

    filename = output_dir / f"{tournament}_{season}_game_ids.txt"

    with open(filename, "w") as f:
        for gid in game_ids:
            f.write(str(gid) + "\n")

    print(f"{tournament} {season}: {len(game_ids)} game_ids saved")

    time.sleep(2)  # ← 2 sekunnin odotus