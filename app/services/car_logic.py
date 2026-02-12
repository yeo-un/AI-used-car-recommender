from typing import List, Dict, Any


def filter_by_budget(cars: List[Dict[str, Any]], budget: int):
    return [c for c in cars if c["price"] <= budget]


def score_vehicle(car: Dict[str, Any], preferences: Dict[str, Any]):
    score = 0

    # 옵션 점수
    for opt in preferences.get("preferred_options", []):
        if opt in car.get("options", []):
            score += 10

    # 연식 조건
    if car.get("year", 0) >= preferences.get("min_year", 0):
        score += 5

    # 주행거리 감점
    score -= car.get("mileage", 0) // 20000

    return score
