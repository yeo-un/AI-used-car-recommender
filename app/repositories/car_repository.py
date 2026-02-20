from sqlalchemy.orm import Session
from app.db.models import Car


class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cars_under_budget(self, budget: int):
        return self.db.query(Car).filter(Car.price <= budget).all()

    def get_all_cars(self):
        return self.db.query(Car).all()
