# Dashboard Tutorial for Digital Twin 
## Initialization



### 1.	Create a folder where we are going to store the app
    
```
    My_folder/Dashboard   
```
    

### 2.	Initialize Github repository ** Optional – Connect with github
```os
    cd My_folder/Dashboard
    git init
    git add .
    git commit -m "Initialize repo"
    git remote add origin https://github.com/username/Dashboard
    git push -u origin master
```

Or you can use VS Code + Github extension. Then go to the github tab and click on the button "Initialize repository"

You will be asked to log in with your github account and write a name for your remote repository.

### 3.	Create intial files in the folder. 

Create a Dashboard.py file for the Streamlit app,
Create a Map.html which will be your map container.

### 4. Create a virtual environment and add packages to it
a.	I have been using UV for package management (a bit easier and cleaner than only pip)

b. On the terminal

```py
    pip install uv      
```
	
For mac 
```
 brew install uv
```
c.	Now to create a virtual environment

```py
    uv venv
```
d. Add packages to the virtual environment

```py
    uv pip install streamlit pandas plotly numpy geopandas json rasterio shapely
```

## Streamlit app setup

### 1.	Create a Streamlit confing file and styling

On your folder where the app is located, create a folder called **.streamlit** and then create a file called **config.toml** and write the following:

```toml

[theme]
primaryColor="#3b80cfff"
backgroundColor="#2a2a2a"
secondaryBackgroundColor="#121212"
textColor="#ffffff"
linkColor="#3b80cfff"
borderColor = "#7c7c7c"
showWidgetBorder = true
font="sans serif"

```

---
## :exclamation:  Make it your own! Change the colors and the font

#### You can see more configuration options in the [docs](https://docs.streamlit.io/develop/api-reference/configuration/config.toml#theme)
---

### 2. Create a secrets file for the app

All the secret information for your app should be stored in a file called **secrets.toml** in your **.streamlit** folder.

We are going to add here our mapbox access token.

```toml
MAPBOX_ACCESS_KEY = "pk.YOURKEYHERE"
```

---
:question: Do you have your own Mapbox access token?
---
---

### 3. Create the Streamlit app basic structure

#### Create sections for your code using comments

```py
# ==== Import packages ====

# ==== Page layout ====

# ==== Read data ===

# ==== Functions ====

# ==== Sidebar ====

# ==== Main panel ====

# ==== Map ====

# ==== Footer ====

```

#### Import packages

```py
import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import json
import geopandas as gpd
```

#### Page layout

On your layout structure we are going to add a title for the page and a sidebar with some options.

Add the following code

```py

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

``` 

#### Create a Title for your app

```py
st.title("DT Dashboard Demo")
```

### First Run

Now we can check that our app is working and everything is set up correctly.

On your terminal run:

```
streamlit run Dashboard.py
```

You should be able to see your app on http://localhost:8501/ or similar.

You will see the title of the app

---
## The Map container



Stremlit has some map options incorporated to create simple maps. But as we are going to add some more features, we are going to create our own map container.

We are going to use a HTML component to create our map container.

### Creating the map

On your **Map.html** file create a basic HTML configuration. On VS code you can just type `html:5` and then `tab` to create the basic skeleton.

Or copy and paste this

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Map view</title>
</head>
<body>
    
</body>
</html>
```
### Adding the Mapbox API
So first we need to include the MapboxGL API and the basic style in our HTML.
On your header of your HTML file add the following

```html
 <link href="https://api.mapbox.com/mapbox-gl-js/v3.15.0/mapbox-gl.css" rel="stylesheet" />
  <script src="https://api.mapbox.com/mapbox-gl-js/v3.15.0/mapbox-gl.js"></script>
```

Now on the body we need to get our secret token from the **secrets.toml** file. We are going to use the following code

```html
<script id="mapbox-key" type="text/plain">__MAPBOX_KEY__</script>
```
Then we create a container div and add a map to it. On our map we want to be able to see a 3D view, so we add a pitch and a beearing.

Use the code below to create your map component. It includes a point layer as a simple example

```html
<div id="map" ></div>
<script>
    mapboxgl.accessToken = document.getElementById('mapbox-key').textContent;

    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [6.52, 52.40],
        pitch: 45,
        beearing: -20,
        zoom: 12
      });

    map.on('load', () => {
        map.addLayer({
          'id': 'points',
          'type': 'circle',
          'source': {
            'type': 'geojson',
            'data': {
              'type': 'FeatureCollection',
              'features': [
                {
                  'type': 'Feature',
                  'geometry': {
                    'type': 'Point',
                    'coordinates': [6.52, 52.40]
                  }
                }
              ]
            }
          },
          'paint': {
            'circle-radius': 10,
            }
        });
      });

```

**Refresh your app and you should see your map.**

### Adding 3D buildings

Now we are going to add 3D models to our map using the information from OpenStreetMap.

So relplace the point layer with a building layer like this:

```js
 map.on('style.load', () => {
        const layers = map.getStyle().layers;
        const labelLayerId = layers.find(
            (layer) => layer.type === 'symbol' && layer.layout['text-field']
        ).id;

        // The 'building' layer in the Mapbox Streets
        // vector tileset contains building height data
        // from OpenStreetMap.
        map.addLayer(
            {
                'id': 'add-3d-buildings',
                'source': 'composite',
                'source-layer': 'building',
                'filter': ['==', 'extrude', 'true'],
                'type': 'fill-extrusion',
                'minzoom': 15,
                'paint': {
                    'fill-extrusion-color': '#aaa',

                    // Use an 'interpolate' expression to
                    // add a smooth transition effect to
                    // the buildings as the user zooms in.
                    'fill-extrusion-height': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        15,
                        0,
                        15.05,
                        ['get', 'height']
                    ],
                    'fill-extrusion-base': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        15,
                        0,
                        15.05,
                        ['get', 'min_height']
                    ],
                    'fill-extrusion-opacity': 0.6
                }
            },
            labelLayerId
        );
    });
```
If you want play with the options of color, height and opacity.

**Refresh your app and you should see your map with 3D buildings.**

---
:warning: Seems like something is not working. What could it be?
---

---


### Sending API key to the map

In our dashboard we need to read the map file and send the access token to the map container.
To do so we can use the following code:

```python
with open("./Map_Lecture.html", 'r', encoding="utf-8") as f:
            mapbox_html = f.read()

mapbox_html = mapbox_html.replace("__MAPBOX_KEY__", MAPBOX_API_KEY)

```
Here we are "sending a text message" to the html file and replacing the text script with the mapbox key.

---
Perhaps you want to change the initial state zoom and the center of the map.

:question: What are the coordinates for the city center of Enschede? 
:question: Which zoom level would be good to set for the map?
---

---
## Read Data

we are going to read 

- SENTINEL HEAT DATA
- add polygon boundary
- crop raster to the extent of the city
- find some NDVI data
- Get max and min indicators
- Create hexagons
- Perform zonal statistics
- Draw polygons on the map
- change values of raster inside polygons
- update indicators

- figure out other indicators