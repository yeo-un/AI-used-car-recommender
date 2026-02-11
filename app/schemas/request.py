from pydantic import BaseModel
from typing import List, Optional


class RecommendationRequest(BaseModel):
    budget: int
    min_year: int
    preferred_options: Optional[List[str]] = []
