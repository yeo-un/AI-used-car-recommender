from typing import List, Dict


# 더미 차량 데이터
DUMMY_CARS = [
    {
        "model": "Hyundai Sonata",
        "price": 1800,
        "year": 2021,
        "options": ["navigation", "rear_camera"],
    },
    {
        "model": "Kia K5",
        "price": 2200,
        "year": 2022,
        "options": ["navigation", "sunroof"],
    },
]


def calculate_score(
    car: Dict, budget: int, min_year: int, preferred_options: List[str]
) -> float:
    score = 0

    # 예산 적합성
    if car["price"] <= budget:
        score += 50

    # 연식
    if car["year"] >= min_year:
        score += 30

    # 옵션 일치
    matched_options = set(preferred_options).intersection(car["options"])
    score += len(matched_options) * 10

    return score


def recommend(budget: int, min_year: int, preferred_options: List[str]):
    results = []

    for car in DUMMY_CARS:
        score = calculate_score(car, budget, min_year, preferred_options)
        results.append(car | {"score": score})  # dict 병합 연산자

    # 점수 기준 정렬
    results.sort(key=lambda x: x["score"], reverse=True)

    return results
