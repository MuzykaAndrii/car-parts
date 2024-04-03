from aiogram.filters.state import State, StatesGroup


class SearchStates(StatesGroup):
    view_results = State()