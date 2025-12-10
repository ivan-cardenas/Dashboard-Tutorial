from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict
import uvicorn

from raster_processing import edit_raster_polygon

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify allowed origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GeoJSONFeature(BaseModel):
    type: str
    geometry: Dict[str, Any]
    properties: Dict[str, Any] | None = None

@app.post("/polygon")
async def receive_polygon(feature: GeoJSONFeature):
    output_raster, stats = edit_raster_polygon(feature.dict(),
                                        raster_path="data/LST_Enschede.tif",
                                        out_path="data/LST_Enschede_modified.tif",
                                        mode="add",
                                        add_value=3                                   
                                        )
    print("Polygon received:", feature, "Output raster:", stats)
    return {"status": "ok", "output": output_raster}

if __name__ == "__main__":
    uvicorn.run("fast_api:app", host="0.0.0.0", port=8000, reload=True)
