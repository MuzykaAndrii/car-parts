import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Select, ScrollingGroup, Button, Row, Group, Start
from aiogram_dialog.widgets.text import Const, Format, Jinja, Case
from aiogram_dialog import Dialog


from common.selectors import cart_is_present
from catalog.states import CatalogStates
from .states import CartStates
from . import actions, messages, callbacks


cart_window = Window(
    Case(
        {True: Jinja(messages.cart_header), False: Const(messages.cart_empty)},
        selector=cart_is_present,
    ),

    Group(
        ScrollingGroup(
            Select(
                Format(messages.cart_product),
                id="cart_product_select",
                item_id_getter=operator.attrgetter("id"),
                items=F["cart"].products,
                on_click=...,
            ),
            id="products_group",
            hide_on_single_page=True,
            width=1,
            height=5,
        ),
        Row(
            Button(Const("🛒 Оформити замовлення"), id="checkout_btn", on_click=...,),
            Start(Const("➕ Додати ще товари"), id="move_to_catalog", state=CatalogStates.car_providers),
        ),
        Row(
            Cancel(Const("❌ Вийти")),
            Button(Const("🗑️ Очистити корзину"), id="clear_cart_btn", on_click=callbacks.clear_cart_clicked),
        ),
        id="cart_products_group",
        when=cart_is_present,
    ),

    state=CartStates.cart_detail,
    getter=actions.get_user_cart,
    parse_mode="HTML",
)


cart_cleared_window = Window(
    Const("Ваша корзина успішно очищена"),
    Start(Const("До каталогу"), id="to_catalog_btn", state=CatalogStates.car_providers),
    Cancel(Const("❌ Вийти")),

    state=CartStates.cart_cleared,
)

# manage_cart_product_window = Window(

# )


cart_dialog = Dialog(
    cart_window,
    # manage_cart_product_window,
    cart_cleared_window,
)