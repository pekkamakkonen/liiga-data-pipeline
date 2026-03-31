import requests
import time
import json
from pathlib import Path

tournament = "playoffs"
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
    game_ids = [line.strip() for line in f]

for gid in game_ids:
    game_data = {
        "game_id": gid,
        "season": season,       # ← lisätty
        "date": None,
        "tournament": tournament,
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
                game_data["date"] = start[:10]
            except KeyError:
                game_data["date"] = None

        time.sleep(2)

    filename = output_dir / f"{gid}.json"

    with open(filename, "w") as f:
        json.dump(game_data, f)

    print(f"Saved: {filename}")