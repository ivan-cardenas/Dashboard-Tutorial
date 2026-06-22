# 🌍 Digital Twin Dashboard Workshop  
### Streamlit · MapboxGL · Landsat LST · FastAPI · Hexagons · Urban Analytics · Digital Twin

![![DOI](https://zenodo.org/badge/1107580356.svg)](https://doi.org/10.5281/zenodo.18144984)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Mapbox](https://img.shields.io/badge/Mapbox-GL%20JS-3A9BDC?logo=mapbox)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![GeoPandas](https://img.shields.io/badge/GeoPandas-0.14+-brightgreen?logo=anaconda)
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

This repository contains all materials for the **Digital Twin Dashboard Lecture**, developed for the  
**University of Twente — ITC Faculty**, by **Iván Cárdenas León** [<img src="https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg" height="20"/>](https://www.linkedin.com/in/ivancardenasleon/) [<img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" height="20"/>](https://orcid.org/0009-0005-0245-633X)

Contact: **[Send email](i.cardenasleon@utwente.nl)**

---

## 📌 Citation

> If you use this dataset, please cite:
~~~
@misc{Cardenas-Leon_Urban_Indicators_Dataset,
author = {Cardenas-Leon, Ivan}
title = {{Digital Twin Dashboard Workshop}},
url = {https://ivan-cardenas.github.io/Dashboard-Tutorial/}
doi = {DOI: 10.5281/zenodo.18144988}
}
~~~
---
## 📜 License

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg


---

## 📚 Overview

This workshop teaches participants how to build a lightweight **Urban Digital Twin** using:

- **Streamlit** for the dashboard  
- **MapboxGL JS** for interactive 3D maps  
- **GeoPandas, Rasterio, Tobler** for geospatial processing  
- **FastAPI** for backend polygon operations  
- **H3 hexagons** for raster aggregation  

---

## 🗂️ Repository Structure

```
.
├── Dashboard.py                 
├── Map_Lecture.html                
├── Scripts/
│   └── LST_Landsat.py
│   └── fast_api.py
│   └── raster_processing.py             
├── data/
│   ├── LST_Enschede.tif         
│   ├── Enschede.geojson         
│   └── Heat_Enschede.json       
├── index.html (Presentation)
├── .streamlit/
│   ├── config.toml              
│   └── secrets.toml             
├── requirements.txt
└── README.md                    
```

---

## 🛠️ Installation

### Create environment with **uv**

```bash
uv venv
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\activate   # Windows
```

### Install dependencies

```bash
uv pip install -r requirements.txt
```


### Add Mapbox API token and a Google Earth Engine project

`.streamlit/secrets.toml`:

```toml
MAPBOX_ACCESS_KEY = "pk.YOUR_MAPBOX_TOKEN"
EE_PROJECT = "YOUR_EE_PROJECT"
```

---

## ▶️ Run Dashboard

```bash
streamlit run Dashboard.py
```

---

## 🛰️ Run FastAPI Backend

```bash
uv run fast_api.py
```

---

## 🧩 Workshop Tasks

- Add a **new dataset** (raster or vector)  
- Add **two indicators**  
- Add **one widget**  
- Add **one chart**  

---

## 🎓 Slides

Open:

```
Index.html
```

Keyboard shortcuts:

- **S** — presenter mode  
- **F** — fullscreen  
- **?** — help
- **ESC** — slide overview  

---
