from typing import List, Dict, Any
from app.services.agent_graph import run_agent


def get_dummy_cars():
    return [
        {
            "id": 1,
            "model": "Avante",
            "price": 1800,
            "year": 2021,
            "mileage": 30000,
            "options": ["sunroof", "hud"],
        },
        {
            "id": 2,
            "model": "Sonata",
            "price": 2200,
            "year": 2020,
            "mileage": 40000,
            "options": ["hud"],
        },
        {
            "id": 3,
            "model": "K5",
            "price": 1900,
            "year": 2019,
            "mileage": 60000,
            "options": ["sunroof"],
        },
    ]


def recommend(budget: int, min_year: int, preferred_options: List[str]):
    cars = get_dummy_cars()

    preferences = {
        "min_year": min_year,
        "preferred_options": preferred_options,
    }

    results = run_agent(
        cars=cars,
        budget=budget,
        preferences=preferences,
    )

    return results
