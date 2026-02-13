def calculate_score(car, available_options, budget, min_year, preferred_options):
    score = 100

    # 예산 (30점)
    if car["price"] > budget:
        score -= 30
    else:
        score -= int((car["price"] / budget) * 30)

    # 연식 (20점)
    if car["year"] < min_year:
        score -= 20

    # 주행거리 (20점)
    mileage_penalty = int((car["mileage"] / 100000) * 20)
    score -= mileage_penalty

    # 옵션 (30점)
    option_score = 30
    for opt in preferred_options:
        if opt not in available_options:
            continue  # 존재하지 않는 옵션은 감점 없음
        if opt not in car["options"]:
            option_score -= 10

    score -= 30 - option_score

    return max(score, 0)
