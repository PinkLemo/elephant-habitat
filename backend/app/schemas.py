from typing import Literal

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    # Bounds match the study area from Chapter 3.1.2 (lat -8 to -26, lon 20 to 36).
    # Rejects out-of-range coordinates before they ever reach the KNN models —
    # not just a security guard, it also stops nonsense predictions for
    # points nowhere near Southern Africa.
    lat: float = Field(ge=-26, le=-8, description="Latitude within the study area")
    lon: float = Field(ge=20, le=36, description="Longitude within the study area")
    season: Literal["wet", "dry"]


class PredictResponse(BaseModel):
    suitability: float
    elevation: float
    dist_to_water_km: float
    ndvi_proxy: float