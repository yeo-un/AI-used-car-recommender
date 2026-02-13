from pydantic import BaseModel
from typing import List


class RecommendationRequest(BaseModel):
    budget: int
    min_year: int
    preferred_options: List[str]
