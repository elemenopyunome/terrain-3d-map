import numpy as np
from pathlib import Path
from PIL import Image

# ==========================================
# PATHS
# ==========================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

IMAGERY_DIR = PROJECT_ROOT / "data" / "imagery_tiles"

OUTPUT_FILE = PROJECT_ROOT / "web" / "assets" / "imagery_texture.png"

TILE_SIZE = 256


# ==========================================
# FIND TILES
# ==========================================

def collect_tiles():

    tiles = []

    for z_dir in IMAGERY_DIR.iterdir():

        for x_dir in z_dir.iterdir():

            x = int(x_dir.name)

            for file in x_dir.iterdir():

                if file.suffix != ".png":
                    continue

                y = int(file.stem)

                tiles.append((x, y, file))

    return tiles


# ==========================================
# BUILD TEXTURE
# ==========================================

def build_texture():

    tiles = collect_tiles()

    if not tiles:
        print("No imagery tiles found")
        return

    xs = sorted(set(t[0] for t in tiles))
    ys = sorted(set(t[1] for t in tiles))

    width = len(xs) * TILE_SIZE
    height = len(ys) * TILE_SIZE

    print("Texture size:", width, "x", height)

    texture = Image.new("RGB", (width, height))

    x_index = {x:i for i,x in enumerate(xs)}
    y_index = {y:i for i,y in enumerate(ys)}

    for x, y, file in tiles:

        img = Image.open(file)

        ix = x_index[x]
        iy = y_index[y]

        x_start = ix * TILE_SIZE
        y_start = iy * TILE_SIZE

        texture.paste(img, (x_start, y_start))

        print("Placed tile:", x, y)

    texture.save(OUTPUT_FILE)

    print("Saved imagery texture:", OUTPUT_FILE)


# ==========================================
# MAIN
# ==========================================

def main():

    build_texture()


if __name__ == "__main__":
    main()