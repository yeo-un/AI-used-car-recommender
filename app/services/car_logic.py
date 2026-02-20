def calculate_score(
    car,
    avg_price,
    budget,
    min_year,
    preferred_options,
):
    score = 0

    # ---------------------------
    # 1. 가격 경쟁력 (40점)
    # avg_price보다 저렴할수록 점수 높음
    # ---------------------------

    if avg_price is not None and avg_price > 0:
        ratio = car["price"] / avg_price

        if ratio <= 0.7:
            price_score = 40

        elif ratio <= 0.85:
            price_score = 35

        elif ratio <= 1.0:
            price_score = 30

        elif ratio <= 1.1:
            price_score = 20

        else:
            price_score = 10

    else:
        price_score = 20  # avg_price 없으면 중립 점수

    score += price_score

    # ---------------------------
    # 2. 예산 적합도 (20점)
    # budget 대비 얼마나 여유 있는지
    # ---------------------------

    budget_ratio = car["price"] / budget

    if budget_ratio <= 0.7:
        budget_score = 20

    elif budget_ratio <= 0.85:
        budget_score = 15

    elif budget_ratio <= 1.0:
        budget_score = 10

    else:
        budget_score = 0

    score += budget_score

    # ---------------------------
    # 3. 연식 점수 (15점)
    # ---------------------------

    year_diff = car["year"] - min_year

    if year_diff >= 3:
        year_score = 15

    elif year_diff >= 1:
        year_score = 10

    elif year_diff >= 0:
        year_score = 5

    else:
        year_score = 0

    score += year_score

    # ---------------------------
    # 4. 주행거리 점수 (15점)
    # ---------------------------

    mileage = car["mileage"]

    if mileage <= 30000:
        mileage_score = 15

    elif mileage <= 60000:
        mileage_score = 10

    elif mileage <= 100000:
        mileage_score = 5

    else:
        mileage_score = 0

    score += mileage_score

    # ---------------------------
    # 5. 옵션 점수 (10점)
    # ---------------------------

    if not preferred_options:
        option_score = 5

    else:
        match = 0

        for opt in preferred_options:
            if opt in (car["options"] or []):
                match += 1

        option_score = int((match / len(preferred_options)) * 10)

    score += option_score

    # ---------------------------
    # 최종 점수
    # ---------------------------

    return int(score)
