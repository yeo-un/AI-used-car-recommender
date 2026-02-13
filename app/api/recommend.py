from fastapi import APIRouter
from app.schemas.request import RecommendationRequest
from app.schemas.response import RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("/recommend", response_model=RecommendationResponse)
async def recommend_car(request: RecommendationRequest):
    service = RecommendationService()

    results = service.execute(
        budget=request.budget,
        min_year=request.min_year,
        preferred_options=request.preferred_options,
    )

    return {"results": results}
