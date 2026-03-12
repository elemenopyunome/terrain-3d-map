import os
import math
import time
import requests
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

OUTPUT_DIR = PROJECT_ROOT / "data" / "imagery_tiles"

# =====================================================
# CONFIGURATION
# =====================================================

# Example location (Dallas)
CENTER_LAT = 32.7767
CENTER_LON = -96.7970

# Zoom level (14 = city scale)
ZOOM = 14

# Radius of tiles around center
RADIUS = 3

# Tile server
TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

# Request headers
HEADERS = {
    "User-Agent": "terrain-3d-map/1.0 (educational terrain project)"
}

# Request delay (avoid hammering servers)
REQUEST_DELAY = 0.5


# =====================================================
# TILE CONVERSION
# =====================================================

def latlon_to_tile(lat, lon, zoom):

    lat_rad = math.radians(lat)

    n = 2 ** zoom

    xtile = int((lon + 180.0) / 360.0 * n)

    ytile = int(
        (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)
        / 2.0
        * n
    )

    return xtile, ytile


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

            print("Failed:", url, "Status:", r.status_code)

    except Exception as e:

        print("Error downloading:", url)
        print(e)

    time.sleep(REQUEST_DELAY)


# =====================================================
# MAIN EXECUTION
# =====================================================

def main():

    print("Output directory:", OUTPUT_DIR)

    center_x, center_y = latlon_to_tile(CENTER_LAT, CENTER_LON, ZOOM)

    print("Center tile:", center_x, center_y)

    for dx in range(-RADIUS, RADIUS + 1):
        for dy in range(-RADIUS, RADIUS + 1):

            x = center_x + dx
            y = center_y + dy

            download_tile(ZOOM, x, y)


if __name__ == "__main__":
    main()