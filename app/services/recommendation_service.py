from sqlalchemy.orm import Session
from app.repositories.car_repository import CarRepository
from app.repositories.price_repository import PriceRepository
from app.services.car_logic import calculate_score
from app.services.llm_service import generate_reason


class RecommendationService:
    def __init__(self, db: Session):
        self.car_repo = CarRepository(db)
        self.price_repo = PriceRepository(db)

    def execute(
        self,
        budget: int,
        min_year: int,
        preferred_options: list[str],
    ):

        # 1. 예산 이하 차량만 필터 (중요)
        cars = self.car_repo.get_cars_under_budget(budget)

        results = []

        for car in cars:
            avg_price = self.price_repo.get_avg_price(car.model)
            score = calculate_score(
                car={
                    "price": car.price,
                    "year": car.year,
                    "mileage": car.mileage,
                    "options": car.options or [],
                },
                avg_price=float(avg_price) if avg_price else None,
                budget=budget,
                min_year=min_year,
                preferred_options=preferred_options,
            )

            car_dict = {
                "id": car.id,
                "model": car.model,
                "price": car.price,
                "year": car.year,
                "mileage": car.mileage,
                "options": car.options or [],
                "score": score,
            }

            car_dict["reason"] = generate_reason(car_dict)

            results.append(car_dict)

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:5]
