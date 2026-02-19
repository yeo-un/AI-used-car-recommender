from collections import defaultdict


def calculate_avg_price(cars):
    """
    모델별 평균 가격 계산
    """
    price_sum = defaultdict(int)
    count = defaultdict(int)

    for car in cars:
        model = car["model"]
        price_sum[model] += car["price"]
        count[model] += 1

    avg_price_map = {}

    for model in price_sum:
        avg_price_map[model] = price_sum[model] / count[model]

    return avg_price_map


def calculate_score(
    car,
    available_options,
    avg_price,
    budget,
    min_year,
    preferred_options,
):
    score = 100

    # 평균 시세 대비 가격 점수 (30점)
    price_ratio = car["price"] / avg_price

    if price_ratio <= 0.8:
        price_penalty = 0
    elif price_ratio <= 1.0:
        price_penalty = int((price_ratio - 0.8) / 0.2 * 15)
    elif price_ratio <= 1.2:
        price_penalty = 15 + int((price_ratio - 1.0) / 0.2 * 15)
    else:
        price_penalty = 30

    score -= price_penalty

    # 예산 초과 패널티
    if car["price"] > budget:
        score -= 20

    # 연식
    if car["year"] < min_year:
        score -= 20

    # 주행거리
    mileage_penalty = int((car["mileage"] / 100000) * 20)
    score -= mileage_penalty

    # 옵션
    option_score = 30

    for opt in preferred_options:
        if opt not in available_options:
            continue

        if opt not in car["options"]:
            option_score -= 10

    score -= 30 - option_score

    return max(score, 0)
