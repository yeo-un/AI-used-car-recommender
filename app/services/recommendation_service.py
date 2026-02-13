from app.repositories.car_repository import CarRepository
from app.services.car_logic import calculate_score
from app.services.llm_service import generate_reason


class RecommendationService:
    def __init__(self):
        self.repo = CarRepository()

    def execute(self, budget, min_year, preferred_options):
        cars = self.repo.get_all_cars()

        results = []

        for car in cars:
            available_options = self.repo.get_available_options(car["model"])

            score = calculate_score(
                car,
                available_options,
                budget,
                min_year,
                preferred_options,
            )

            car_with_score = {**car, "score": score}
            car_with_score["reason"] = generate_reason(car_with_score)

            results.append(car_with_score)

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:3]
