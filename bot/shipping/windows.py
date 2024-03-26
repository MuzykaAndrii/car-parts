from aiogram import F
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets import text, kbd, input


from backend.schemas import CreateShippingSchema
from modules.shemainput.schemainput import SchemaInput
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


shipping_address_schema_input = SchemaInput(
    schema=CreateShippingSchema,
    on_end=callbacks.save_shipping_data,
    show_mode=ShowMode.DELETE_AND_SEND,
    invalid_input_msg="Введено неправильні дані, повторіть ще раз",
)


enter_shipping_component_window = Window(
    text.Format("{item.message}"),
    input.TextInput(
        id="shipping_component",
        on_success=shipping_address_schema_input.handle_input,
    ),
    kbd.Cancel(text.Const("Скасувати")),
    state=ShippingStates.shipping_component_entering,
    getter=shipping_address_schema_input.getter,
)


shipping_dialog = Dialog(
    shipping_detail_window,
    enter_shipping_component_window,
)