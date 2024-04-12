import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Select, ScrollingGroup, Button, Row, Group, Start, Back, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja, Case
from aiogram_dialog import Dialog


from common.selectors import cart_is_present, cart_is_not_present
from common import messages as cm
from catalog.states import CatalogStates
from .states import CartStates
from . import actions, messages, callbacks


cart_window = Window(
    Case(
        {True: Jinja(messages.cart_header), False: Const(cm.cart_empty)},
        selector=cart_is_present,
    ),

    Group(
        ScrollingGroup(
            Select(
                Format(messages.cart_product),
                id="cart_product_select",
                item_id_getter=operator.attrgetter("id"),
                items=F["cart"].products,
                on_click=callbacks.cart_product_clicked,
            ),
            id="products_group",
            hide_on_single_page=True,
            width=1,
            height=5,
        ),
        Row(
            Button(Const("🛒 Оформити замовлення"), id="checkout_btn", on_click=callbacks.checkout_clicked),
            Start(Const("➕ Додати ще товари"), id="move_to_catalog", state=CatalogStates.car_providers),
        ),
        Row(
            Cancel(Const("❌ Вийти")),
            Button(Const("🗑️ Очистити корзину"), id="clear_cart_btn", on_click=callbacks.clear_cart_clicked),
        ),
        id="cart_products_group",
        when=cart_is_present,
    ),
    Cancel(Const("❌ Вийти"), when=cart_is_not_present),


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

manage_cart_item_window = Window(
    Jinja(messages.cart_item_detail),

    Button(Const("Видалити"), id="delete_cart_product_btn", on_click=callbacks.delete_cart_product_clicked),
    Row(
        Cancel(Const("❌ Вийти")),
        Back(Const("↩️ До корзини")),
    ),

    state=CartStates.manage_product,
    getter=actions.get_cart_item_details,
    parse_mode="HTML",
)


cart_item_deleted = Window(
    Case(
        {True: Const(messages.product_deleted), False: Const(messages.product_not_deleted)},
        selector=F["dialog_data"]["is_deleted"],
    ),
    SwitchTo(Const("↩️ До корзини"), id="to_cart_from_deleted", state=CartStates.cart_detail),
    Cancel(Const("❌ Вийти")),
    state=CartStates.product_deleted,
)


cart_dialog = Dialog(
    cart_window,
    manage_cart_item_window,
    cart_cleared_window,
    cart_item_deleted,
)