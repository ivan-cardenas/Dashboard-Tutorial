import ee
import geemap
import geopandas as gpd
import streamlit as st
ee.Authenticate()
ee.Initialize(project=st.secrets["GEE_PROJECT"])
print(ee.String('Hello from the Earth Engine servers!').getInfo())

# ---------------------------
# 1) Load City boundary
# ---------------------------
def get_city_boundary(city_name:str):
    dataset = ee.FeatureCollection("WM/geoLab/geoBoundaries/600/ADM2")

    # Select Enschede
    enschede = dataset.filter(ee.Filter.eq("shapeName", city_name))
    enschede_boundary = geemap.ee_to_geojson(enschede)
    enschede_gdf = gpd.GeoDataFrame.from_features(enschede_boundary["features"])
    enschede_gdf.to_file(f"data/{city_name}_boundaries.geojson", driver="GeoJSON")
    
    return enschede

# ---------------------------
# 2) Load Landsat 9 data
# ---------------------------
def generate_LST(city):
    img = (
    ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
    .filterBounds(get_city_boundary("Enschede"))
    .filterDate("2024-05-01", "2024-08-31")
    )

    print("Images found:", img.size().getInfo())

    # Use the maximum pixel value across time (same as img.max() in JS)
    max = img.max().clip(city)

    # ---------------------------
    # 3) Convert ST_B10 → LST (°C)
    # ---------------------------

    bt = max.select("ST_B10")

    # Convert using USGS LST formula (scaled brightness temperature)
    lst = (
        bt.multiply(0.00341802)
        .add(149.0)
        .subtract(273.15)   # Kelvin → °C
    )

    print("LST image:", lst.getInfo())
    
    return lst



def save_LST(city, lst, output_tif):
    output_tif = f"data/LST_{city}.tif"
    city_bounds = get_city_boundary("Enschede")
    lst = generate_LST(city_bounds)
    
    geemap.ee_export_image(
        lst,
        filename=output_tif,
        scale=30,
        region=city_bounds.geometry(),
        file_per_band=False
    )
    
    print(f"Saved local GeoTIFF: {output_tif}")