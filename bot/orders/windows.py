from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Jinja, Case

from common.selectors import cart_is_present
from .states import OrderStates
from . import messages



checkout_window = Window(
    Case(
        {True: Jinja(messages.cart_checkout), False: Const(messages.cart_empty)},
        selector=cart_is_present,
    ),
    state=OrderStates.checkout,
    parse_mode="HTML",
)

order_dialog = Dialog(
    checkout_window,
)