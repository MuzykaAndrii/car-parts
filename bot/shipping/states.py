from aiogram.filters.state import State, StatesGroup


class ShippingStates(StatesGroup):
    show = State()
    change = State()

    shipping_component_entering = State()