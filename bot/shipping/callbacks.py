from typing import Any

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput


from components import backend_service
from .states import ShippingStates


async def handle_shipping_input(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, shipping_component: Any):
    dialog_manager.show_mode=ShowMode.DELETE_AND_SEND

    current = dialog_manager.dialog_data.get("current")
    to_fill_remain = dialog_manager.dialog_data.get("to_fill")
    #TODO: add type checking
    current.value = shipping_component

    dialog_manager.dialog_data.get("filled").append(current)

    if not to_fill_remain:
        fields = dict()
        for filled in dialog_manager.dialog_data.get("filled"):
            fields.update({filled.field_name: filled.value})

        return await save_shipping_data(message.from_user.id, dialog_manager, **fields)

    await dialog_manager.switch_to(ShippingStates.shipping_component_entering)


async def save_shipping_data(user_id: int, manager: DialogManager, **fields):
    account = await backend_service().get_account(user_id)
    await backend_service().create_user_shipping(
        user_id=account.user.id,
        **fields,
    )

    start_data = manager.start_data
    if start_data and start_data.get("move_to"):
        return await manager.start(start_data.get("move_to"))

    await manager.switch_to(ShippingStates.show)


async def invalid_data_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error):
    await message.reply("Введено неправильні дані, повторіть ще раз")