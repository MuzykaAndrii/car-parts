from aiogram.filters.state import State, StatesGroup


class CartStates(StatesGroup):
    cart_detail = State()
    cart_cleared = State()