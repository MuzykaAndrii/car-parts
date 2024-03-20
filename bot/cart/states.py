from aiogram.filters.state import State, StatesGroup


class CartStates(StatesGroup):
    cart_detail = State()
    manage_product = State()
    cart_cleared = State()