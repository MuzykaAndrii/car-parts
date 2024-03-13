import operator

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, Select, Back, Button, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format, Jinja, Case
from aiogram_dialog import Dialog

from .states import CartStates
from . import actions, messages


def cart_is_present(data: dict, case: Case, manager: DialogManager) -> bool:
    return bool(data.get("cart", None))

cart_window = Window(
    Case(
        {
            True: Jinja(messages.cart_checkout),
            False: Const("Ваша корзина поки порожня("),
        },
        selector=cart_is_present,
    ),
    state=CartStates.cart_detail,
    getter=actions.get_user_cart,
    parse_mode="HTML",
)

cart_dialog = Dialog(
    cart_window,
)