import shutil
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt

from utils.paths import COUNTRIES_GPKG,COUNTRY_HIGHLIGHT_IMAGES_DIR
from utils.images.map_drawing_tools import crosses_antimeridian, get_local_projection, prepare_world

def main():
    draw_highlight_maps()

def draw_highlight_maps():

    print("\n===== Drawing country highlight images =====")

    gdf = gpd.read_file(COUNTRIES_GPKG, columns=["ISO_A3", "geometry", "NAM_0"],)

    output_dir = Path(COUNTRY_HIGHLIGHT_IMAGES_DIR)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    total = len(gdf)

    for i, (_, country) in enumerate(gdf.iterrows(), start=1):

        iso3 = country["ISO_A3"]

        if not isinstance(iso3, str):
            continue

        iso3 = iso3.upper()
        name = country["NAM_0"]

        print(f"\r\033[KDrawing {iso3} ({name}) ({i}/{total})...", end="", flush=True)

        # Handle dateline countries
        use_dateline_shift = crosses_antimeridian(country.geometry)
        working_gdf = prepare_world(gdf, use_dateline_shift)

        target_geometry = working_gdf.loc[country.name, "geometry"]

        # Create local projection
        local_crs = get_local_projection(target_geometry)

        # Determine viewing window in geographic coordinates first
        minx, miny, maxx, maxy = target_geometry.bounds

        width = maxx - minx
        height = maxy - miny
        size = max(width, height)

        padding = size * 0.5

        # Select nearby countries before projection
        nearby_geo = working_gdf.cx[
            minx - padding:maxx + padding,
            miny - padding:maxy + padding
        ]

        # Project only the relevant countries
        nearby = nearby_geo.to_crs(local_crs)
        target = nearby.loc[[country.name]]

        # Determine viewing window in projected coordinates
        minx, miny, maxx, maxy = target.total_bounds

        width = maxx - minx
        height = maxy - miny

        size = max(width, height)

        padding = size * 0.5

        cx = (minx + maxx) / 2
        cy = (miny + maxy) / 2

        half = size / 2 + padding

        xmin = cx - half
        xmax = cx + half
        ymin = cy - half
        ymax = cy + half

        # Plot
        fig, ax = plt.subplots(figsize=(6, 6))

        nearby.plot(
            ax=ax,
            color="lightgrey",
            edgecolor="black",
            linewidth=0.2,
        )

        target.plot(
            ax=ax,
            color="#46923c",
            edgecolor="black",
            linewidth=0.4,
        )

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_aspect("equal")
        ax.set_axis_off()

        plt.savefig(
            output_dir / f"{iso3}.png",
            dpi=400,
            bbox_inches="tight",
            pad_inches=0,
            transparent=True,
        )

        plt.close(fig)

    print("\r\033[KDone!", end="", flush=True)


if __name__ == "__main__":
    main()