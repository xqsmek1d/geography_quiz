import shutil
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

from shapely.geometry import MultiPolygon
from shapely import get_coordinates
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from utils.assets.map_drawing_tools import INSET_COUNTRIES, ZOOM_COUNTRIES, crosses_antimeridian, shift_longitudes
from utils.paths import COUNTRIES_GPKG, COUNTRY_HIGHLIGHT_IMAGES_DIR

PADDING_FACTOR = 0.1

def main():
    draw_globe_highlights()

def remove_small_polygons(geometry, min_area=1e-5):
    if geometry.geom_type == "MultiPolygon":
        polygons = [
            poly
            for poly in geometry.geoms
            if poly.area > min_area
        ]

        return MultiPolygon(polygons)

    return geometry

def get_country_extent(geometry, padding_factor=PADDING_FACTOR):

    minx, miny, maxx, maxy = geometry.bounds

    width = maxx - minx
    height = maxy - miny

    padding = max(width, height) * padding_factor

    return (
        minx - padding,
        maxx + padding,
        miny - padding,
        maxy + padding,
    )
    
def add_country_inset(fig, geometry):
    
    if crosses_antimeridian(geometry):
        #print("CROSSES ANTIMERIDIAN")
        geometry = shift_longitudes(geometry)

    minx, miny, maxx, maxy = geometry.bounds
    #print(f"geometry bounds: {geometry.bounds}")

    centre_lon = (minx + maxx) / 2

    projection = ccrs.PlateCarree(central_longitude=centre_lon)

    inset = fig.add_axes([0.05, 0.05, 0.35, 0.35], projection=projection)
    
    #size = max(maxx - minx, maxy - miny)
    #padding = max(size * PADDING_FACTOR, 0.02)
    extent = get_country_extent(geometry)

    #print(f"plotting extent: {extent}")

    inset.set_extent(
        extent,
        crs=ccrs.PlateCarree(),
    )

    inset.add_feature(
        cfeature.OCEAN,
        facecolor="#a6cee3",
    )

    inset.add_feature(
        cfeature.LAND,
        facecolor="lightgrey",
    )

    inset.add_feature(
        cfeature.COASTLINE.with_scale("50m"),
        linewidth=0.2,
    )

    inset.add_geometries(
        [geometry],
        crs=ccrs.PlateCarree(),
        facecolor="#46923c",
        edgecolor="black",
        linewidth=0.3,
    )

    inset.set_xticks([])
    inset.set_yticks([])
    return inset

def add_inset_rectangle(ax, geometry):
    
    if crosses_antimeridian(geometry):
        geometry = shift_longitudes(geometry)

    minx, miny, maxx, maxy = geometry.bounds

    padding = max(maxx - minx, maxy - miny) * PADDING_FACTOR

    rect = Rectangle(
        (minx - padding, miny - padding),
        (maxx - minx) + 2 * padding,
        (maxy - miny) + 2 * padding,
        fill=False,
        edgecolor="black",
        linewidth=1.0,
        transform=ccrs.PlateCarree(),
    )

    ax.add_patch(rect)
    return rect

def connect_inset(ax, fig, inset, rect):

    rect_corners = rect.get_corners()

    globe_corners = []

    for corner in rect_corners:
        lon, lat = corner

        display = ax.transData.transform(
            ax.projection.transform_point(
                lon,
                lat,
                ccrs.PlateCarree()
            )
        )

        figure = fig.transFigure.inverted().transform(display)

        globe_corners.append(tuple(figure))

    # Get inset corners in figure coordinates
    bbox = inset.get_position()

    inset_corners = [
        (bbox.x0, bbox.y0),
        (bbox.x1, bbox.y0),
        (bbox.x1, bbox.y1),
        (bbox.x0, bbox.y1),
    ]

    connections = [
    (globe_corners[1], inset_corners[1]),
    (globe_corners[3], inset_corners[3]),
    ]

    for start, end in connections:
        line = Line2D(
            [start[0], end[0]],
            [start[1], end[1]],
            transform=fig.transFigure,
            color="black",
            linewidth=0.8,
        )

        fig.add_artist(line)

def draw_globe_highlights():
    check = input("Do you want to (re)create the country highlight images, considering this MAY TAKE A WHILE? (Y/n): ")
    
    if check != "Y":
        return
        
    print("\n===== Drawing globe country images =====")

    gdf = gpd.read_file(
        COUNTRIES_GPKG,
        columns=["ISO_A3", "geometry", "NAM_0"],
    )

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

        print(f"\r\033[KDrawing {iso3} ({name}) ({i}/{total})...", end="", flush=True,)

        # Country centre
        centroid = country.geometry.representative_point()
        lon = centroid.x
        lat = centroid.y

        # Create globe projection
        if iso3 in ZOOM_COUNTRIES:
            projection = ccrs.NearsidePerspective(central_latitude=lat, central_longitude=lon, satellite_height=5000000.0)
        else:
            projection = ccrs.NearsidePerspective(central_latitude=lat, central_longitude=lon, satellite_height=10000000.0)

        # Highlight country
        geometry = country.geometry
        geometry = remove_small_polygons(geometry)
        
        fig = plt.figure(figsize=(6, 6))

        ax = plt.axes(projection=projection)
        
        ax.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor="#a6cee3")
        ax.add_feature(cfeature.LAND.with_scale("50m"),  facecolor="lightgrey")
        ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.2,)
        ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.2,)
        ax.gridlines()

        ax.add_geometries(
            [geometry],
            crs=ccrs.PlateCarree(),
            facecolor="#46923c",
            edgecolor="black",
            linewidth=0.3,
        )

        if iso3 in INSET_COUNTRIES:
            rect = add_inset_rectangle(ax, geometry)
            inset = add_country_inset(fig, geometry)
            if inset:
                connect_inset(ax, fig, inset, rect)

        ax.set_global()
        ax.set_aspect("equal")

        output_path = output_dir / f"{iso3}.png"
        output_path.unlink(missing_ok=True)

        plt.savefig(
            output_path,
            dpi=300,
            #bbox_inches="tight",
            #pad_inches=0,
            transparent=True,
        )

        plt.close(fig)

    print("\r\033[KDone!", flush=True)

if __name__ == "__main__":
    main()