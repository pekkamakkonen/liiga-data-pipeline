import requests
import time
import json
from pathlib import Path
from datetime import datetime, timezone

tournament = "runkosarja"
season = 2025

game_ids_file = f"data/raw/game_ids/{tournament}_{season}_game_ids.txt"

output_dir = Path(f"data/raw/games/{tournament}_{season}")
output_dir.mkdir(parents=True, exist_ok=True)

base_urls = {
    "game": "https://liiga.fi/api/v2/games",
    "stats": "https://liiga.fi/api/v2/games/stats",
    "shotmap": "https://liiga.fi/api/v2/shotmap"
}

with open(game_ids_file) as f:
    game_ids = [int(line.strip()) for line in f]

for gid in game_ids:
    game_data = {
        "game_id": gid,
        "season": season,
        "tournament": tournament,
        "game_date": None,
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "data": {}
    }

    for key, base in base_urls.items():
        url = f"{base}/{season}/{gid}"

        r = requests.get(url)
        r.raise_for_status()
        response_json = r.json()

        game_data["data"][key] = response_json

        if key == "game":
            try:
                start = response_json["game"]["start"]
                game_data["game_date"] = start[:10]
            except KeyError:
                game_data["game_date"] = None

        time.sleep(2)

    filename = output_dir / f"{gid}.json"

    with open(filename, "w") as f:
        json.dump(game_data, f)

    print(f"Saved: {filename}")