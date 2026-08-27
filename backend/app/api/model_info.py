from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/model/info")
def model_info(request: Request) -> dict:
    engine = request.app.state.engine
    meta = engine.metadata
    return {
        "trained_at": meta["trained_at"],
        "sklearn_version": meta["sklearn_version"],
        "auc_mean": meta["spatial_cv_auc_mean"],
        "auc_std": meta["spatial_cv_auc_std"],
        "feature_importances": meta["feature_importances"],
        "n_training_records": meta["n_training_records"],
    }