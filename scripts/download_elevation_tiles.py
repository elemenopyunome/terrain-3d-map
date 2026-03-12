import os
import time
import requests
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

IMAGERY_DIR = PROJECT_ROOT / "data" / "imagery_tiles"
OUTPUT_DIR = PROJECT_ROOT / "data" / "elevation_tiles"

# =====================================================
# CONFIG
# =====================================================

# Terrarium elevation tiles
TILE_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

HEADERS = {
    "User-Agent": "terrain-3d-map/1.0 elevation downloader"
}

REQUEST_DELAY = 0.3


# =====================================================
# DOWNLOAD FUNCTION
# =====================================================

def download_tile(z, x, y):

    url = TILE_URL.format(z=z, x=x, y=y)

    folder = OUTPUT_DIR / str(z) / str(x)
    os.makedirs(folder, exist_ok=True)

    filepath = folder / f"{y}.png"

    if filepath.exists():
        print("Skipping existing:", filepath)
        return

    try:

        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code == 200:

            with open(filepath, "wb") as f:
                f.write(r.content)

            print("Downloaded:", filepath)

        else:

            print("Failed:", url, r.status_code)

    except Exception as e:

        print("Error:", url)
        print(e)

    time.sleep(REQUEST_DELAY)


# =====================================================
# FIND IMAGERY TILES
# =====================================================

def find_imagery_tiles():

    tiles = []

    for z_dir in IMAGERY_DIR.iterdir():

        if not z_dir.is_dir():
            continue

        z = int(z_dir.name)

        for x_dir in z_dir.iterdir():

            x = int(x_dir.name)

            for file in x_dir.iterdir():

                if file.suffix != ".png":
                    continue

                y = int(file.stem)

                tiles.append((z, x, y))

    return tiles


# =====================================================
# MAIN
# =====================================================

def main():

    print("Scanning imagery tiles...")

    tiles = find_imagery_tiles()

    print("Tiles found:", len(tiles))

    for z, x, y in tiles:

        download_tile(z, x, y)


if __name__ == "__main__":
    main()