import random

models = {
    "Morning": {
        "price": (500, 1200),
        "options": ["heated_seat", "navigation"],
    },
    "Avante": {
        "price": (800, 2200),
        "options": ["sunroof", "hud", "heated_seat", "navigation"],
    },
    "K5": {
        "price": (1000, 2500),
        "options": ["sunroof", "hud", "heated_seat", "ventilated_seat", "navigation"],
    },
    "Sonata": {
        "price": (1200, 2800),
        "options": ["sunroof", "hud", "heated_seat", "ventilated_seat", "navigation"],
    },
    "Grandeur": {
        "price": (1800, 4000),
        "options": ["sunroof", "hud", "heated_seat", "ventilated_seat", "navigation"],
    },
}

cars = []

id_counter = 1

for _ in range(100):
    model = random.choice(list(models.keys()))

    price_range = models[model]["price"]
    available_options = models[model]["options"]

    price = random.randint(price_range[0], price_range[1])
    year = random.randint(2015, 2023)
    mileage = random.randint(5000, 150000)

    option_count = random.randint(0, len(available_options))
    options = random.sample(available_options, option_count)

    cars.append(
        {
            "id": id_counter,
            "model": model,
            "price": price,
            "year": year,
            "mileage": mileage,
            "options": options,
        }
    )

    id_counter += 1


# 옵션 메타데이터
model_option_metadata = {model: data["options"] for model, data in models.items()}
