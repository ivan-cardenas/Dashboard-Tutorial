# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **Digital Twin Dashboard** workshop built for the University of Twente (ITC Faculty). It visualizes Land Surface Temperature (LST) over Enschede using Streamlit, MapboxGL JS, Google Earth Engine, and H3 hexagons.

## Running the Project

### Setup (uv)
```bash
uv venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

uv pip install -r requirements.txt
```

### Required secrets — `.streamlit/secrets.toml`
```toml
MAPBOX_API_KEY = "pk.YOUR_MAPBOX_TOKEN"
GEE_PROJECT = "YOUR_GEE_PROJECT_ID"
```

### Run the Streamlit dashboard
```bash
streamlit run Dashboard.py
```

### Run the FastAPI backend (optional, for polygon editing)
```bash
uv run Scripts/fast_api.py
```

## Architecture

```
Dashboard.py            # Streamlit entry point
Scripts/
  LST_Landsat.py        # Google Earth Engine: fetch Landsat 9 LST and export GeoTIFF
  fast_api.py           # FastAPI server on port 8000: receives drawn polygons, edits raster
  raster_processing.py  # Core raster editing logic (multiply/add/set values inside polygon)
Map_Lecture.html        # MapboxGL JS template — contains __MAPBOX_KEY__, __PET_ENSCHEDE__, __HEXAGONS__ placeholders
data/
  Enschede_boundaries.geojson
  LST_Enschede.tif      # Landsat LST raster (pre-downloaded, used by default)
  Heat_Enschede.json    # PET (Physiological Equivalent Temperature) hexagon data
.streamlit/
  config.toml           # Dark theme settings
  secrets.toml          # API keys (not committed)
```

### Data flow

1. **Dashboard.py** loads `Enschede_boundaries.geojson` and `LST_Enschede.tif` at startup.
2. The sidebar's H3 resolution slider triggers `create_hexagons()` (using `tobler.h3fy`) and `calculate_stats()` (zonal stats via `rasterio.mask`) to aggregate LST into hexagons.
3. `build_map_html()` injects the Mapbox key, PET GeoJSON, and hexagon GeoJSON into `Map_Lecture.html` template placeholders, which is then rendered via `st.components.v1.components.html`.
4. The optional FastAPI backend (`Scripts/fast_api.py`) listens on `POST /polygon` for GeoJSON features drawn in Mapbox Draw, then calls `edit_raster_polygon()` to modify pixel values in `LST_Enschede.tif` and write `LST_Enschede_modified.tif`.
5. `Scripts/LST_Landsat.py` handles on-demand data refresh from Google Earth Engine — it authenticates with `ee.Authenticate()` and exports Landsat 9 Band 10 (ST_B10) imagery converted to °C.

### Key design notes

- `load_data()` in Dashboard.py is wrapped with `@st.cache_data` to avoid re-fetching from GEE on every rerender.
- The map template uses string replacement (not Jinja2) — `__MAPBOX_KEY__`, `__PET_ENSCHEDE__`, and `__HEXAGONS__` are literal placeholder strings in `Map_Lecture.html`.
- The FastAPI backend is a standalone process; the dashboard does not call it directly — the MapboxGL JS frontend makes the fetch to `localhost:8000/polygon`.
- GEE authentication (`ee.Authenticate()`) runs at module import time in `LST_Landsat.py` — this will prompt interactively if credentials are not cached.
- Data files in `data/` are pre-generated; the GEE pipeline only needs to run when refreshing the source imagery.
