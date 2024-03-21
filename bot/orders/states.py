from aiogram.filters.state import State, StatesGroup


class OrderStates(StatesGroup):
    checkout = State()
    submitted = State()