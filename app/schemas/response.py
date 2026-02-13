from pydantic import BaseModel
from typing import List


class CarResponse(BaseModel):
    id: int
    model: str
    price: int
    year: int
    mileage: int
    options: List[str]
    score: int
    reason: str


class RecommendationResponse(BaseModel):
    results: List[CarResponse]
