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
    kbd.SwitchTo(text.Const("Вказати адресу"), id="cerate_shipping", state=ShippingStates.first_name, when=shipping_not_available),

    kbd.Cancel(text.Const("Вийти")),
    getter=actions.get_user_shipping,
    state=ShippingStates.show,
    parse_mode="HTML",
)


enter_firstname_window = Window(
    text.Const("Введіть ваше імя"),
    input.TextInput(
        id="enter_firstname",
        type_factory=str,
        on_success=callbacks.firstname_handler,
        on_error=callbacks.invalid_data_handler,
    ),
    kbd.Cancel(text.Const("Скасувати")),
    state=ShippingStates.first_name,
)

enter_lastname_window = Window(
    text.Const("Введіть ваше прізвище"),
    input.TextInput(
        id="enter_lastname",
        type_factory=str,
        on_success=callbacks.lastname_handler,
        on_error=callbacks.invalid_data_handler,
    ),
    kbd.Cancel(text.Const("Скасувати")),
    state=ShippingStates.last_name,
)

enter_phone_window = Window(
    text.Const("Введіть ваш номер телефону"),
    input.TextInput(
        id="enter_phonenumber",
        type_factory=int,
        on_success=callbacks.phone_handler,
        on_error=callbacks.invalid_data_handler,
    ),
    kbd.Cancel(text.Const("Скасувати")),
    state=ShippingStates.phone_number,
)

enter_region_window = Window(
    text.Const("Введіть область"),
    input.TextInput(
        id="enter_region",
        type_factory=str,
        on_success=callbacks.region_handler,
        on_error=callbacks.invalid_data_handler,
    ),
    kbd.Cancel(text.Const("Скасувати")),
    state=ShippingStates.region,
)

enter_city_window = Window(
    text.Const("Введіть населений пункт"),
    input.TextInput(
        id="enter_city",
        type_factory=str,
        on_success=callbacks.city_handler,
        on_error=callbacks.invalid_data_handler,
    ),
    kbd.Cancel(text.Const("Скасувати")),
    state=ShippingStates.city,
)

enter_office_number_window = Window(
    text.Const("Введіть номер відділення НП"),
    input.TextInput(
        id="enter_officenumber",
        type_factory=int,
        on_success=callbacks.office_number_handler,
        on_error=callbacks.invalid_data_handler,
    ),
    kbd.Cancel(text.Const("Скасувати")),
    state=ShippingStates.office_number,
)


shipping_dialog = Dialog(
    shipping_detail_window,
    enter_firstname_window,
    enter_lastname_window,
    enter_phone_window,
    enter_region_window,
    enter_city_window,
    enter_office_number_window,
)