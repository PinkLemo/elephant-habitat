from fastapi import APIRouter, Request

from app.core.limiter import limiter
from app.schemas import PredictRequest, PredictResponse

router = APIRouter()


# Plain `def`, not `async def` — predict_proba() is blocking CPU work.
# FastAPI runs sync route functions in a threadpool automatically, so one
# slow prediction doesn't stall the event loop for every other concurrent
# request. Making this `async def` without manually offloading the model
# call would be the wrong choice here.
@router.post("/predict/point", response_model=PredictResponse)
@limiter.limit("30/minute")
def predict_point(request: Request, body: PredictRequest) -> PredictResponse:
    engine = request.app.state.engine
    result = engine.predict(lat=body.lat, lon=body.lon, season=body.season)
    return PredictResponse(**result)