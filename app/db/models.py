from sqlalchemy import Column, Integer, String, JSON, Numeric, TIMESTAMP, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(100), nullable=False, index=True)
    price = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)
    mileage = Column(Integer, nullable=False)
    options = Column(JSON, nullable=True)


class CarPriceStats(Base):
    __tablename__ = "car_price_stats"

    model = Column(String(100), primary_key=True)
    avg_price = Column(Numeric, nullable=False)
    count = Column(Integer, nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )
