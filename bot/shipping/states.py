from aiogram.filters.state import State, StatesGroup


class ShippingStates(StatesGroup):
    show = State()
    create = State()