import random
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

"""
중고차 더미 데이터 생성기.

차량 라인(아반떼, 소나타 등)별로 세대(모델)를 두고 세대마다 연식 범위·가격 범위를 조사 기반으로 정의
각 세대 내에서만 연식/가격을 랜덤 조합, 가격이 비쌀수록 옵션 개수를 많게 부여
(크롤링 대신 사용)

---------------------------------------------------------------------------
차량 라인별 세대(모델) 정의
- 설정 파일: `app/db/car_lines.json`
- 스키마: line_name → { generations: [ { name, year_range, price_range, mileage_range, options_pool, ... } ] }
---------------------------------------------------------------------------
"""


def _load_car_lines_json() -> Dict[str, Dict[str, Any]] | None:
    """
    `app/db/car_lines.json`를 로드
    실패하거나 스키마가 다르면 None을 반환
    """
    path = Path(__file__).resolve().with_name("car_lines.json")
    if not path.exists():
        return None

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not isinstance(raw, dict):
        return None

    # 최소 스키마 검증 + 타입 정규화(list → tuple)
    try:
        for _line_name, line in raw.items():
            gens = line.get("generations")
            if not isinstance(gens, list) or not gens:
                raise ValueError("missing generations")

            for gen in gens:
                if not isinstance(gen, dict):
                    raise ValueError("generation must be dict")

                for k in (
                    "name",
                    "year_range",
                    "price_range",
                    "mileage_range",
                    "options_pool",
                ):
                    if k not in gen:
                        raise ValueError(f"missing key: {k}")

                yr = gen["year_range"]
                pr = gen["price_range"]
                mr = gen["mileage_range"]
                op = gen["options_pool"]

                if (
                    not isinstance(yr, (list, tuple))
                    or len(yr) != 2
                    or not isinstance(pr, (list, tuple))
                    or len(pr) != 2
                    or not isinstance(mr, (list, tuple))
                    or len(mr) != 2
                    or not isinstance(op, list)
                ):
                    raise ValueError("invalid range/options types")

                gen["year_range"] = (int(yr[0]), int(yr[1]))
                gen["price_range"] = (int(pr[0]), int(pr[1]))
                gen["mileage_range"] = (int(mr[0]), int(mr[1]))
                gen["options_pool"] = [str(x) for x in op]
    except Exception:
        return None

    return raw


CAR_LINES = _load_car_lines_json()
if not CAR_LINES:
    raise RuntimeError("car_lines data not loaded.")


# def _option_count_by_price(
#     price: int,
#     min_p: int,
#     max_p: int,
#     pool_size: int,
# ) -> int:
#     """
#     가격이 비쌀수록 옵션 개수를 많게 한다.
#     해당 세대 가격 구간 내 비율에 따라 0 ~ pool_size 개 선형 부여.
#     """
#     if max_p <= min_p:
#         return random.randint(0, min(pool_size, 2))
#     ratio = (price - min_p) / (max_p - min_p)
#     count = int(ratio * pool_size)
#     count = max(0, min(count, pool_size))
#     count = count + random.randint(-1, 1)
#     return max(0, min(count, pool_size))


def _pick_generation() -> Tuple[str, str, Dict[str, Any]]:
    """라인명, 모델명(라인 + 세대), 해당 세대 메타를 무작위로 반환."""
    line_name = random.choice(list(CAR_LINES.keys()))
    line = CAR_LINES[line_name]
    gen = random.choice(line["generations"])
    model_name = f"{line_name} {gen['name']}"
    return line_name, model_name, gen


def _compute_price(
    year: int,
    year_range: Tuple[int, int],
    mileage: int,
    mileage_range: Tuple[int, int],
    opt_count: int,
    pool_size: int,
    price_range: Tuple[int, int],
) -> int:
    """
    연식이 최신에 가까울수록, 주행거리가 적을수록, 옵션이 많을수록 가격이 높아지도록,
    0~1 스코어로 정규화한 뒤 세대별 가격 구간 내에서 매핑
    """
    min_y, max_y = year_range
    min_m, max_m = mileage_range
    min_p, max_p = price_range

    # 연식 요인: 같은 세대 내에서 최신 연식일수록 1에 가깝게
    if max_y <= min_y:
        f_year = 0.5
    else:
        f_year = (year - min_y) / (max_y - min_y)
        f_year = max(0.0, min(f_year, 1.0))

    # 주행거리 요인: 같은 세대 내에서 적게 탄 차량일수록 1에 가깝게
    if max_m <= min_m:
        f_mileage = 0.5
    else:
        f_mileage = 1.0 - (mileage - min_m) / (max_m - min_m)
        f_mileage = max(0.0, min(f_mileage, 1.0))

    # 옵션 요인: 풀옵션에 가까울수록 1에 가깝게
    if pool_size <= 0:
        f_options = 0.0
    else:
        f_options = opt_count / pool_size
        f_options = max(0.0, min(f_options, 1.0))

    # 가중합으로 스코어 계산 (가중치는 필요 시 튜닝 가능)
    score = 0.4 * f_year + 0.3 * f_mileage + 0.3 * f_options

    # 세대별 가격 구간 안에서 선형 매핑 + 약간의 노이즈
    base_price = min_p + score * (max_p - min_p)
    noise_span = (max_p - min_p) * 0.05  # ±5% 정도 랜덤
    price = base_price + random.uniform(-noise_span, noise_span)

    # 정수화 및 클램핑
    price_int = int(round(price))
    return max(min_p, min(max_p, price_int))


def generate_cars(n: int = 150, seed: int | None = None) -> List[Dict[str, Any]]:
    """
    n대의 중고차 더미 데이터를 생성한다.
    - 차량은 라인·세대를 랜덤 선택 후, 해당 세대의 연식/가격/주행거리 범위 안에서만 랜덤.
    - 옵션은 같은 세대 내에서 비쌀수록 많게 부여.
    """
    if seed is not None:
        random.seed(seed)

    out: List[Dict[str, Any]] = []
    id_counter = 1

    for _ in range(n):
        _line, model_name, gen = _pick_generation()
        min_y, max_y = gen["year_range"]
        min_m, max_m = gen["mileage_range"]
        pool = gen["options_pool"]
        min_p, max_p = gen["price_range"]
        pool_size = len(pool)

        year = random.randint(min_y, max_y)
        mileage = random.randint(min_m, max_m)

        # 연식이 최신에 가까울수록 옵션 개수를 많이 주도록
        if pool_size > 0:
            if max_y <= min_y:
                year_ratio = 0.5
            else:
                year_ratio = (year - min_y) / (max_y - min_y)
                year_ratio = max(0.0, min(year_ratio, 1.0))

            # 옵션 기대값: 기본 30% + 연식 비율 따라 최대 100%까지
            mean_opt = 0.3 * pool_size + 0.7 * pool_size * year_ratio
            spread = int(0.3 * pool_size)
            low = max(0, int(mean_opt) - spread)
            high = min(pool_size, int(mean_opt) + spread)
            if low > high:
                low, high = high, high
            opt_count = random.randint(low, high)
        else:
            opt_count = 0

        options = random.sample(pool, opt_count) if opt_count > 0 else []

        price = _compute_price(
            year=year,
            year_range=(min_y, max_y),
            mileage=mileage,
            mileage_range=(min_m, max_m),
            opt_count=opt_count,
            pool_size=pool_size,
            price_range=(min_p, max_p),
        )

        out.append(
            {
                "id": id_counter,
                "model": model_name,
                "price": price,
                "year": year,
                "mileage": mileage,
                "options": options,
            }
        )
        id_counter += 1

    return out


# import 시 자동 생성 (150대)
cars = generate_cars(n=150, seed=42)

# 옵션 메타: "라인 세대" 형태 모델명 → 해당 세대 옵션 풀 (API/프론트 참고용)
model_option_metadata: Dict[str, List[str]] = {}
for line_name, line in CAR_LINES.items():
    for gen in line["generations"]:
        model_option_metadata[f"{line_name} {gen['name']}"] = gen["options_pool"]
