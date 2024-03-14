from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, Counter, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja, Case
from aiogram_dialog import Dialog

from .states import CartStates
from . import actions, messages, callbacks


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

enter_amount_window = Window(
    Format("Введіть бажану кількість товару:"),
    Counter(
        id="amount_counter",
        default=1,
        min_value=1,
        max_value=50,
        plus=Const("➕"),
        minus=Const("➖"),
        text=Format("Додати {value:g}шт."),
        on_text_click=callbacks.amount_entered,
    ),
    Cancel(Const("Вийти")),
    state=CartStates.enter_amount,
)

cart_dialog = Dialog(
    cart_window,
    enter_amount_window,
)