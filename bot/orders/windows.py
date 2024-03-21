from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Jinja, Case
from aiogram_dialog.widgets import kbd

from catalog.states import CatalogStates
from common.selectors import cart_is_present
from common import messages as cm
from .states import OrderStates
from . import messages, actions



checkout_window = Window(
    Case(
        {True: Jinja(messages.cart_checkout), False: Const(cm.cart_empty)},
        selector=cart_is_present,
    ),

    kbd.Row(
        kbd.Button(Const("Замовити"), id="make_order_btn", on_click=...,),
        kbd.Start(Const("Додати товари"), id="to_catalog_btn", state=CatalogStates.car_providers),
    ),
    kbd.Cancel(Const("Вийти")),
    
    getter=actions.get_checkout_data,
    state=OrderStates.checkout,
    parse_mode="HTML",
)

order_dialog = Dialog(
    checkout_window,
)