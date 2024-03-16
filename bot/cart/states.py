from aiogram.filters.state import State, StatesGroup


class CartStates(StatesGroup):
    cart_detail = State()
    checkout = State()
    enter_amount = State()
    cart_cleared = State()