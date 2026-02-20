from sqlalchemy.orm import Session
from app.db.models import CarPriceStats


class PriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_avg_price(self, model: str):

        stat = self.db.query(CarPriceStats).filter(CarPriceStats.model == model).first()

        if stat:
            return stat.avg_price

        return None
