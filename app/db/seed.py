from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Car, CarPriceStats
from app.db.dummy_data import cars

"""
실행 방법: uv run python -m app.db.seed

cars seeded
price stats seeded
-------------------
cars already seeded
price stats already seeded
"""


def seed_cars(db: Session):

    existing = db.query(Car).first()

    if existing:
        print("cars already seeded")
        return

    for car in cars:
        db_car = Car(
            id=car["id"],
            model=car["model"],
            price=car["price"],
            year=car["year"],
            mileage=car["mileage"],
            options=car["options"],
        )
        db.add(db_car)

    db.commit()

    print("cars seeded")


def seed_price_stats(db: Session):

    existing = db.query(CarPriceStats).first()

    if existing:
        print("price stats already seeded")
        return

    stats = {}

    for car in cars:
        model = car["model"]
        if model not in stats:
            stats[model] = {
                "total": 0,
                "count": 0,
            }
        stats[model]["total"] += car["price"]
        stats[model]["count"] += 1

    for model, data in stats.items():
        avg_price = data["total"] / data["count"]
        stat = CarPriceStats(
            model=model,
            avg_price=avg_price,
            count=data["count"],
        )
        db.add(stat)

    db.commit()
    print("price stats seeded")


def run_seed():

    db = SessionLocal()

    try:
        seed_cars(db)
        seed_price_stats(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
