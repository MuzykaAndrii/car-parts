from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets import text, kbd, input

from .states import ShippingStates
from . import actions, messages, callbacks


shipping_available = F["shipping"]
shipping_not_available = ~shipping_available


shipping_detail_window = Window(
    text.Jinja(messages.shipping_detail, when=shipping_available),
    # kbd.SwitchTo(text.Const("Змінити дані"), id="change_shipping_btn", state=ShippingStates.change),

    text.Const("Ви не вказали поки що дані доставки.", when=shipping_not_available),
    kbd.SwitchTo(text.Const("Вказати адресу"), id="cerate_shipping", state=ShippingStates.shipping_component_entering, when=shipping_not_available),

    kbd.Cancel(text.Const("Вийти")),
    getter=actions.get_user_shipping,
    state=ShippingStates.show,
    parse_mode="HTML",
)


enter_shipping_component_window = Window(
    text.Format("{component.message}"),
    input.TextInput(
        id="shipping_component",
        on_success=callbacks.handle_shipping_input,
        on_error=callbacks.invalid_data_handler,
    ),
    kbd.Cancel(text.Const("Скасувати")),
    state=ShippingStates.shipping_component_entering,
    getter=actions.get_shipping_component,
)


shipping_dialog = Dialog(
    shipping_detail_window,
    enter_shipping_component_window,
)