from aiogram.filters.state import State, StatesGroup


class ShippingStates(StatesGroup):
    show = State()
    change = State()

    first_name = State()
    last_name = State()
    phone_number = State()
    region = State()
    city = State()
    office_number = State()