from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
def health(request: Request) -> dict:
    engine = getattr(request.app.state, "engine", None)
    return {"status": "ok", "model_loaded": engine is not None}