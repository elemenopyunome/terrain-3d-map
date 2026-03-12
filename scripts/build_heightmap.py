import numpy as np
from pathlib import Path
from PIL import Image

# =====================================================
# PROJECT PATHS
# =====================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

ELEVATION_DIR = PROJECT_ROOT / "data" / "elevation_tiles"
OUTPUT_DIR = PROJECT_ROOT / "data"

HEIGHTMAP_FILE = OUTPUT_DIR / "heightmap.npy"
HEIGHTMAP_IMAGE = OUTPUT_DIR / "heightmap.png"

TILE_SIZE = 256


# =====================================================
# TERRARIUM HEIGHT DECODER
# =====================================================

def decode_height(pixel):

    r, g, b = pixel

    r = int(r)
    g = int(g)
    b = int(b)

    height = (r * 256 + g + b / 256) - 32768

    return height


# =====================================================
# LOAD TILE
# =====================================================

def load_tile(tile_path):

    img = Image.open(tile_path)

    pixels = np.array(img)

    heightmap = np.zeros((TILE_SIZE, TILE_SIZE))

    for y in range(TILE_SIZE):
        for x in range(TILE_SIZE):

            r, g, b = pixels[y, x]

            heightmap[y, x] = decode_height((r, g, b))

    return heightmap


# =====================================================
# FIND ALL TILES
# =====================================================

def collect_tiles():

    tiles = []

    for z_dir in ELEVATION_DIR.iterdir():

        z = int(z_dir.name)

        for x_dir in z_dir.iterdir():

            x = int(x_dir.name)

            for file in x_dir.iterdir():

                if file.suffix != ".png":
                    continue

                y = int(file.stem)

                tiles.append((z, x, y, file))

    return tiles


# =====================================================
# BUILD HEIGHTMAP
# =====================================================

def build_heightmap():

    tiles = collect_tiles()

    if not tiles:
        print("No elevation tiles found")
        return

    print("Tiles found:", len(tiles))

    xs = sorted(set(t[1] for t in tiles))
    ys = sorted(set(t[2] for t in tiles))

    width = len(xs) * TILE_SIZE
    height = len(ys) * TILE_SIZE

    print("Final heightmap size:", width, "x", height)

    heightmap = np.zeros((height, width))

    x_index = {x: i for i, x in enumerate(xs)}
    y_index = {y: i for i, y in enumerate(ys)}

    for z, x, y, file in tiles:

        tile_heights = load_tile(file)

        ix = x_index[x]
        iy = y_index[y]

        x_start = ix * TILE_SIZE
        y_start = iy * TILE_SIZE

        heightmap[y_start:y_start + TILE_SIZE,
                  x_start:x_start + TILE_SIZE] = tile_heights

        print("Processed tile:", x, y)

    return heightmap


# =====================================================
# SAVE OUTPUT
# =====================================================

def save_heightmap(heightmap):

    np.save(HEIGHTMAP_FILE, heightmap)

    print("Saved heightmap array:", HEIGHTMAP_FILE)

    # normalize for preview image
    min_h = np.min(heightmap)
    max_h = np.max(heightmap)

    normalized = (heightmap - min_h) / (max_h - min_h)

    img = (normalized * 255).astype(np.uint8)

    Image.fromarray(img).save(HEIGHTMAP_IMAGE)

    print("Saved preview image:", HEIGHTMAP_IMAGE)


# =====================================================
# MAIN
# =====================================================

def main():

    heightmap = build_heightmap()

    if heightmap is not None:

        save_heightmap(heightmap)


if __name__ == "__main__":
    main()