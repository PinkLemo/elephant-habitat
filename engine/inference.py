"""
engine/inference.py

Loads the three models serialized in the notebook (Cell 20) and exposes a
single `predict()` method that the FastAPI route calls per request.

Loading happens once, at import time — not per-request — so a prediction
call is just: Haversine (cheap) + two KNN lookups + one RF forward pass.
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path
from typing import Literal, TypedDict

import joblib

MODELS_DIR = Path(__file__).parent / "models"

# Same seven water bodies from Cell 9 of the notebook — must stay in sync
# if you ever add/remove water features and retrain.
MAJOR_WATER = [
    (-18.9249, 26.1658),  # Okavango Delta, Botswana
    (-17.9243, 25.8572),  # Zambezi River
    (-16.1000, 28.9500),  # Lake Kariba
    (-19.0000, 23.5000),  # Okavango River
    (-18.0000, 31.5000),  # Limpopo River
    (-15.0000, 28.0000),  # Kafue River, Zambia
    (-22.6500, 27.1167),  # Limpopo, Botswana
]


class PredictionResult(TypedDict):
    suitability: float
    elevation: float
    dist_to_water_km: float
    ndvi_proxy: float


def _haversine_km(lat: float, lon: float, water_points: list[tuple[float, float]]) -> float:
    """Minimum great-circle distance from (lat, lon) to any point in water_points."""
    min_dist = float("inf")
    for wlat, wlon in water_points:
        dlat = math.radians(wlat - lat)
        dlon = math.radians(wlon - lon)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat)) * math.cos(math.radians(wlat)) * math.sin(dlon / 2) ** 2
        )
        dist = 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        min_dist = min(min_dist, dist)
    return min_dist


class HabitatInferenceEngine:
    """
    Loads rf_final, knn_elev, knn_ndvi once at startup.

    Usage:
        engine = HabitatInferenceEngine()
        result = engine.predict(lat=-18.7, lon=24.6, season="wet")
    """

    def __init__(self, models_dir: Path = MODELS_DIR):
        rf_path = models_dir / "rf_final.pkl"
        knn_elev_path = models_dir / "knn_elev.pkl"
        knn_ndvi_path = models_dir / "knn_ndvi.pkl"
        metadata_path = models_dir / "metadata.json"

        for path in (rf_path, knn_elev_path, knn_ndvi_path, metadata_path):
            if not path.exists():
                raise FileNotFoundError(
                    f"Missing model artifact: {path}. "
                    "Run the serialization cell in the notebook first."
                )

        self.rf_model = joblib.load(rf_path)
        self.knn_elev = joblib.load(knn_elev_path)
        self.knn_ndvi = joblib.load(knn_ndvi_path)

        with open(metadata_path) as f:
            self.metadata = json.load(f)

        # The exact column order rf_final was trained on — never hardcode
        # this a second time, always read it from metadata.
        self.feature_order: list[str] = self.metadata["feature_order"]

    def predict(self, lat: float, lon: float, season: Literal["wet", "dry"]) -> PredictionResult:
        dist_to_water_km = _haversine_km(lat, lon, MAJOR_WATER)

        # KNeighborsRegressor expects a 2D array: one row, two columns [lat, lon]
        point = [[lat, lon]]
        elevation = float(self.knn_elev.predict(point)[0])
        ndvi_proxy = float(self.knn_ndvi.predict(point)[0])
        season_encoded = 1 if season == "wet" else 0

        feature_values = {
            "elevation": elevation,
            "dist_to_water_km": dist_to_water_km,
            "season_encoded": season_encoded,
            "ndvi_proxy": ndvi_proxy,
        }

        # Build the row in the exact order the model was trained on.
        # rf_final was fit on a DataFrame (with column names), so predicting
        # from a plain list triggers a benign "no feature names" UserWarning
        # on every call — silenced narrowly here rather than hiding all
        # sklearn warnings, so anything else it warns about still surfaces.
        ordered_row = [[feature_values[name] for name in self.feature_order]]
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="X does not have valid feature names")
            suitability = float(self.rf_model.predict_proba(ordered_row)[0][1])

        return {
            "suitability": round(suitability, 4),
            "elevation": round(elevation, 1),
            "dist_to_water_km": round(dist_to_water_km, 1),
            "ndvi_proxy": round(ndvi_proxy, 4),
        }