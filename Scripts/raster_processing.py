
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import geometry_mask
from shapely.geometry import shape
import geopandas as gpd


def edit_raster_polygon(
    feature: dict,
    raster_path: str,
    out_path: str,
    mode: str = "multiply",
    factor: float = 1.1,
    add_value: float = 10.0,
    new_value: float | None = None,
):
    """
    Edit pixel values INSIDE a polygon and return updated stats.

    Parameters
    ----------
    feature : dict
        GeoJSON Feature (single polygon) from Mapbox Draw (EPSG:4326).
    raster_path : str
        Path to input raster.
    out_path : str
        Path to output raster.
    mode : str
        How to edit pixels inside polygon:
            - "multiply": multiply by factor
            - "add": add add_value
            - "set": set to new_value
    factor : float
        Factor for "multiply" mode.
    add_value : float
        Value for "add" mode.
    new_value : float | None
        Constant value for "set" mode.

    Returns
    -------
    out_path : str
        Output raster path.
    stats : dict
        Dict of statistics for the WHOLE raster AFTER modification
        (ignoring NoData).
    """

    raster_path = Path(raster_path)
    out_path = Path(out_path)

    # ---- 1. Open raster ----
    with rasterio.open(raster_path) as src:
        # For simplicity assume single-band; extend to multi-band if needed
        data = src.read(1)  # (height, width)
        transform = src.transform
        raster_crs = src.crs
        nodata = src.nodata

        # ---- 2. Build polygon in raster CRS ----
        geom = shape(feature["geometry"])  # in EPSG:4326 (lon/lat from Mapbox)
        gdf = gpd.GeoDataFrame(
            {"id": [1]},
            geometry=[geom],
            crs="EPSG:4326"
        )

        if gdf.crs != raster_crs:
            gdf = gdf.to_crs(raster_crs)

        geom_proj = gdf.geometry.iloc[0]

        # ---- 3. Build mask for "inside polygon" ----
        # geometry_mask returns True for pixels OUTSIDE by default.
        # invert=True => True INSIDE polygon.
        inside_mask = geometry_mask(
            [geom_proj.__geo_interface__],
            transform=transform,
            out_shape=data.shape,
            invert=True
        )

        # inside_mask is a boolean array (True where we want to edit)
        # Make a copy to avoid modifying original array accidentally
        edited = data.copy()

        # ---- 4. Apply your chosen modification INSIDE the polygon ----
        if mode == "multiply":
            edited[inside_mask] = edited[inside_mask] * factor
        elif mode == "add":
            edited[inside_mask] = edited[inside_mask] + add_value
        elif mode == "set":
            if new_value is None:
                raise ValueError("new_value must be given for mode='set'")
            edited[inside_mask] = new_value
        else:
            raise ValueError(f"Unknown mode: {mode}")

        # Optional: if raster is integer, you may want to cast back:
        # edited = edited.astype(data.dtype)

        # ---- 5. Write the edited raster ----
        meta = src.meta.copy()
        with rasterio.open(out_path, "w", **meta) as dst:
            dst.write(edited, 1)

    # ---- 6. Compute statistics over the WHOLE raster (ignoring NoData) ----
    # Use the edited array we already have (no need to reopen)
    arr = edited.astype("float64")  # avoid overflow issues
    if nodata is not None:
        arr[arr == nodata] = np.nan

    valid = ~np.isnan(arr)
    if not valid.any():
        stats = {k: None for k in ["min", "max", "mean", "std", "p5", "p50", "p95"]}
    else:
        vals = arr[valid]
        stats = {
            "min": float(np.nanmin(vals)),
            "max": float(np.nanmax(vals)),
            "mean": float(np.nanmean(vals)),
            "std": float(np.nanstd(vals)),
            "p5": float(np.nanpercentile(vals, 5)),
            "p50": float(np.nanpercentile(vals, 50)),  # median
            "p95": float(np.nanpercentile(vals, 95)),
        }

    return str(out_path), stats
