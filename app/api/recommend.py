from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.request import RecommendationRequest
from app.schemas.response import RecommendationResponse
from app.services.recommendation_service import RecommendationService
from app.db.session import get_db

router = APIRouter()


@router.post("/recommend", response_model=RecommendationResponse)
def recommend_car(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)

    results = service.execute(
        budget=request.budget,
        min_year=request.min_year,
        preferred_options=request.preferred_options,
    )

    return {"results": results}
