import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import json
import rasterio
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

def load_data(city:str, path:str):
    city_bounds =get_city_boundary(city)
    lst = generate_LST(city_bounds)
    save_LST(city, lst, path) 

def handle_load_button(city:str, path:str):
    # 1) load data
    load_data(city, path=path)
    # 2) update hex JSON that will be inserted into template
    st.session_state.hex_json = HEXAGONS.to_json()


def create_hexagons(city:gpd, resolution:int, local_crs):
    print("Creating hexagons...")
    hexes = h3fy(city, resolution=10, clip=True)
        
    hex_wgs84 = hexes.to_crs(epsg=4326)
    
    print("Hexagons created:", hex_wgs84.size)
    return hex_wgs84
    
def build_map_html(pet_json: str, hex_json: str) -> str:
    html = mapbox_html.replace("__MAPBOX_KEY__", MAPBOX_API_KEY)
    html = html.replace("__PET_ENSCHEDE__", pet_json)
    html = html.replace("__HEXAGONS__", hex_json)
    return html
    
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

HEXAGONS = create_hexagons(CITY_BOUNDARY, 10, 28992)


with open("./Map_Lecture.html", 'r', encoding="utf-8") as f:
            mapbox_html = f.read()

# =======================
# SIDEBAR
# =======================
with st.sidebar:
    st.button("Load data", on_click=(handle_load_button), args=("Enschede", "./data/LST_Enschede.tif"))
    


# =======================
# MAIN PAGE
# =======================
st.title("🏙️ Digital Twin Dashboard Demo")


# =======================
# MAP WINDOW
# =======================
if "hex_json" not in st.session_state:
    st.session_state.hex_json = HEXAGONS.to_json()
    
st.session_state.layer_visible = True

    
hex_json = st.session_state.hex_json

mapbox_html = build_map_html(PET_ENSCHEDE_HEX.to_json(), st.session_state.hex_json)

components.html(
    mapbox_html,
    height=600,
)
    

# =======================
# FOOTER
# =======================