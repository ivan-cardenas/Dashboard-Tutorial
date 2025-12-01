import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import json

# ============================================================================
# Page layout
# ===========================================================================
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================
# CONSTANTS & FIXED DATA
# =======================
# DATA = pd.read_csv("", index_col=0)

MAPBOX_API_KEY = st.secrets.get("MAPBOX_API_KEY")
if MAPBOX_API_KEY is None:
    st.error("Mapbox token not configured")
    


# =======================
# SIDEBAR
# =======================


# =======================
# MAIN PAGE
# =======================
st.title("🏙️ Digital Twin Dashboard Demo")


# =======================
# MAP WINDOW
# =======================

with open("./Map_Lecture.html", 'r', encoding="utf-8") as f:
            mapbox_html = f.read()

mapbox_html = mapbox_html.replace("__MAPBOX_KEY__", MAPBOX_API_KEY)

components.html(
    mapbox_html,
    height=600,
)

# =======================
# FOOTER
# =======================