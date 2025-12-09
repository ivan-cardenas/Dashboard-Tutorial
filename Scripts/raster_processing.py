# raster_processing.py
import json
from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import shape

def apply_polygon_mask(feature: dict) -> str:
    """
    feature: dict with keys type, geometry, properties (GeoJSON Feature)
    Returns path to modified raster.
    """
    # --- 1. Read raster ---
    raster_path = Path("data/LST_Enschede.tif")   # <- your raster here
    out_path = Path("data/output_raster_masked.tif")

    with rasterio.open(raster_path) as src:
        raster_crs = src.crs

        # --- 2. Build GeoDataFrame from GeoJSON feature ---
        geom = shape(feature["geometry"])
        gdf = gpd.GeoDataFrame(
            {"id": [1]},
            geometry=[geom],
            crs="EPSG:4326"  # Mapbox gives WGS84 lon/lat
        )

        # Reproject to raster CRS if needed
        if gdf.crs != raster_crs:
            gdf = gdf.to_crs(raster_crs)

        # mask() expects geometries as GeoJSON-like dicts in raster CRS
        geoms = [json.loads(gdf.to_json())["features"][0]["geometry"]]

        # --- 3. Mask raster with polygon ---
        # crop=True => output extent is the polygon bbox
        # invert=False => keep inside polygon, hide outside
        out_image, out_transform = mask(src, geoms, crop=True, invert=False)
        out_meta = src.meta.copy()

    # --- 4. Update metadata and write ---
    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    with rasterio.open(out_path, "w", **out_meta) as dest:
        dest.write(out_image)

    return str(out_path)
