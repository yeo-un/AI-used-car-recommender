from pydantic import BaseModel
from typing import List


class RecommendationRequest(BaseModel):
    budget: int
    min_year: int = 2015
    preferred_options: List[str] = []
