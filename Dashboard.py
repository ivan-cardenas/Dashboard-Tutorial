import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import json
import rasterio
from rasterio.mask import mask
import math
import shapely
from tobler.util import h3fy
from Scripts.LST_Landsat import get_city_boundary, generate_LST, save_LST

# ============================================================================
# Page layout
# ===========================================================================
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===========================================================================
# FUNCTIONS
# ===========================================================================
@st.cache_data
def load_data(city:str, path:str):
    city_bounds =get_city_boundary(city)
    lst = generate_LST(city_bounds)
    save_LST(city, lst, path) 

def handle_load_button(city:str, path:str):
    # 1) load data
    load_data(city, path=path)
    # 2) update hex JSON that will be inserted into template
    st.session_state.hex_json = HEXAGONS.to_json()


def create_hexagons(city:gpd, resolution:int,):
    print("Creating hexagons...")
    hexes = h3fy(city, resolution, clip=True)
        
    hex_wgs84 = hexes.to_crs(epsg=4326)
    
    print("Hexagons created:", hex_wgs84.size)
    return hex_wgs84
    
def build_map_html(pet_json: str, hex_json: str) -> str:
    html = mapbox_html.replace("__MAPBOX_KEY__", MAPBOX_API_KEY)
    html = html.replace("__PET_ENSCHEDE__", pet_json)
    html = html.replace("__HEXAGONS__", hex_json)
    return html

def calculate_stats(raster_path:str, zones:gpd, stat:str):
    print("Calculating stats...")
    raster = rasterio.open(raster_path)
    def derive_stats(geom, data, **mask_kw):
        masked, mask_transform = mask(dataset=data, shapes=(geom,),
                                    crop=True, all_touched=True, filled=True)
        return masked
    
    zones[stat] = zones.geometry.apply(derive_stats, data=raster).apply(np.mean)
    print("Stats calculated:", zones.size)
    return zones

# =======================
# CONSTANTS & FIXED DATA
# =======================
# DATA = pd.read_csv("", index_col=0)

MAPBOX_API_KEY = st.secrets.get("MAPBOX_API_KEY")
if MAPBOX_API_KEY is None:
    st.error("Mapbox token not configured")
    

    
CITY_BOUNDARY = gpd.read_file("./data/Enschede_boundaries.geojson")

LST_ENSCHEDE = rasterio.open("./data/LST_Enschede.tif") 

PET_ENSCHEDE_HEX = gpd.read_file("./data/Heat_Enschede.json")




with open("./Map_Lecture.html", 'r', encoding="utf-8") as f:
            mapbox_html = f.read()

# =======================
# SIDEBAR
# =======================
with st.sidebar:
    st.markdown("## Parameters")
    hex_res = st.slider("Select resolution", 1, 12, 8, key="resolution")
    if hex_res:
        with st.spinner("Loading hexagons..."):
            hexes = create_hexagons(CITY_BOUNDARY, hex_res)
            HEXAGONS = calculate_stats("./data/LST_Enschede.tif", hexes, "mean").to_json()



# =======================
# VARIABLES
# =======================

max_lst = round(LST_ENSCHEDE.read(1).max(),2)
min_lst = round(LST_ENSCHEDE.read(1).min(),2)
mean_lst = round(LST_ENSCHEDE.read(1).mean(),2)

hexes = create_hexagons(CITY_BOUNDARY, hex_res)
HEXAGONS = calculate_stats("./data/LST_Enschede.tif", hexes, "mean").to_json()

    


# =======================
# MAIN PAGE
# =======================
st.title("🏙️ Digital Twin Dashboard Demo")


# =======================
# MAP WINDOW
# =======================

mapbox_html = build_map_html(PET_ENSCHEDE_HEX.to_json(), HEXAGONS)

components.html(
    mapbox_html,
    height=800,
)
    
col1, col2, col3 = st.columns(3)

with col1 as col:
    st.metric("Max LST", f"{max_lst}°C", delta=f"{1.5}°C")
    


col2.metric("Min LST", f"{min_lst}°C", delta=f"{0}°C")
col3.metric("Mean LST", f"{mean_lst}°C", delta=f"{-0.24} °C")


# =======================
# FOOTER
# =======================