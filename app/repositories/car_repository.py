from app.db.dummy_data import cars, model_option_metadata


class CarRepository:
    def get_all_cars(self):
        return cars

    def get_available_options(self, model: str):
        return model_option_metadata.get(model, [])
