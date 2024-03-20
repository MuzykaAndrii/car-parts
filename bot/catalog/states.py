from aiogram.filters.state import State, StatesGroup


class CatalogStates(StatesGroup):
    car_providers = State()
    cars_list = State()
    car_parts = State()
    part_item = State()
    enter_amount = State()
    added = State()