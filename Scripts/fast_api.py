from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict
import uvicorn

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
    print("Polygon received:", feature)
    return {"status": "ok", "received": feature}

if __name__ == "__main__":
    uvicorn.run("fast_api:app", host="0.0.0.0", port=8000, reload=True)
