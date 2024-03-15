import operator
from aiogram import F
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, Counter, Select, ScrollingGroup, Button, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja, Case
from aiogram_dialog import Dialog

from .states import CartStates
from . import actions, messages, callbacks


def cart_is_present(data: dict, case: Case, manager: DialogManager) -> bool:
    return bool(data.get("cart", None))

checkout_window = Window(
    Case(
        {
            True: Jinja(messages.cart_checkout),
            False: Const("Ваша корзина поки порожня("),
        },
        selector=cart_is_present,
    ),
    state=CartStates.checkout,
    getter=actions.get_user_cart,
    parse_mode="HTML",
)


cart_window = Window(
    Jinja(messages.cart_header),
    ScrollingGroup(
        Select(
            Format(messages.cart_product),
            id="cart_product_select",
            item_id_getter=lambda item: item.part.id,
            # item_id_getter=F.part.id,
            items=F["cart"].products,
            on_click=...,
        ),
        id="products_group",
        hide_on_single_page=True,
        width=1,
        height=5,
    ),
    Row(
        Button(
            Const("🛒 Оформити замовлення"),
            id="checkout_btn",
            on_click=...,
        ),
        Button(
            Const("➕ Додати ще товари"),
            id="add_products_btn",
            on_click=...,
        ),
    ),
    Row(
        Cancel(Const("❌ Вийти")),
        Button(
            Const("🗑️ Очистити корзину"),
            id="clear_cart_btn",
            on_click=...,
        ),
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
    checkout_window,
    enter_amount_window,
)