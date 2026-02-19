from app.repositories.car_repository import CarRepository
from app.repositories.price_repository import PriceRepository
from app.services.car_logic import calculate_score
from app.services.llm_service import generate_reason


class RecommendationService:
    def __init__(self):
        self.car_repo = CarRepository()
        self.price_repo = PriceRepository()

    def execute(self, budget, min_year, preferred_options, limit=3):
        cars = self.car_repo.get_all_cars()

        avg_price_map = self.price_repo.get_avg_price_map()

        scored_results = []

        # 1️⃣ Hard filtering + score 계산 (LLM 호출 없음)
        for car in cars:
            # Hard constraint: 예산
            if car["price"] > budget:
                continue

            # Hard constraint: 연식
            if car["year"] < min_year:
                continue

            available_options = self.car_repo.get_available_options(car["model"])

            avg_price = avg_price_map.get(car["model"], car["price"])

            score = calculate_score(
                car,
                available_options,
                avg_price,
                budget,
                min_year,
                preferred_options,
            )

            scored_results.append(
                {
                    **car,
                    "score": score,
                }
            )

        # 결과 없으면 즉시 반환
        if not scored_results:
            return []

        # 2️⃣ score 기준 정렬
        scored_results.sort(key=lambda x: x["score"], reverse=True)

        # 3️⃣ Top N 선택
        top_results = scored_results[:limit]

        # 4️⃣ Top N만 LLM reason 생성 (비용 최적화 핵심)
        final_results = []

        for car in top_results:
            reason = generate_reason(car)

            final_results.append(
                {
                    **car,
                    "reason": reason,
                }
            )

        return final_results
