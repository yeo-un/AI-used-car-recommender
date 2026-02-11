from fastapi import APIRouter
from app.schemas.request import RecommendationRequest
from app.services.recommender import recommend

router = APIRouter()


@router.post("/recommend")
async def recommend_car(request: RecommendationRequest):
    results = recommend(
        budget=request.budget,
        min_year=request.min_year,
        preferred_options=request.preferred_options,
    )

    return {"results": results}
