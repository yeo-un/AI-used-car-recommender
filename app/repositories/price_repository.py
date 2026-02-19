from collections import defaultdict
from app.repositories.car_repository import CarRepository


class PriceRepository:
    """
    현재: dummy_data 기반 aggregate
    미래: PostgreSQL aggregate table 조회로 교체 예정
    """

    def __init__(self):
        self.car_repo = CarRepository()

    def get_avg_price_map(self):
        cars = self.car_repo.get_all_cars()

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

    def get_avg_price(self, model: str):
        avg_map = self.get_avg_price_map()
        return avg_map.get(model)
