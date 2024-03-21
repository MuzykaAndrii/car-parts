from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput


from components import backend_service
from .states import ShippingStates


async def firstname_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, firstname: str):
    dialog_manager.show_mode=ShowMode.DELETE_AND_SEND
    dialog_manager.dialog_data.update(first_name=firstname)
    await dialog_manager.next()


async def lastname_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, lastname: str):
    dialog_manager.show_mode=ShowMode.DELETE_AND_SEND
    dialog_manager.dialog_data.update(last_name=lastname)
    await dialog_manager.next()


async def phone_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, phone: int):
    dialog_manager.show_mode=ShowMode.DELETE_AND_SEND
    dialog_manager.dialog_data.update(phone_number=phone)
    await dialog_manager.next()


async def region_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, region: str):
    dialog_manager.show_mode=ShowMode.DELETE_AND_SEND
    dialog_manager.dialog_data.update(region=region)
    await dialog_manager.next()


async def city_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, city: str):
    dialog_manager.show_mode=ShowMode.DELETE_AND_SEND
    dialog_manager.dialog_data.update(city=city)
    await dialog_manager.next()


async def office_number_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, office_number: int):
    dialog_manager.show_mode=ShowMode.DELETE_AND_SEND

    account = await backend_service().get_account(message.from_user.id)
    await backend_service().create_user_shipping(
        user_id=account.user.id,
        first_name=dialog_manager.dialog_data.get("first_name"),
        last_name=dialog_manager.dialog_data.get("last_name"),
        phone_number=dialog_manager.dialog_data.get("phone_number"),
        region=dialog_manager.dialog_data.get("region"),
        city=dialog_manager.dialog_data.get("city"),
        office_number=office_number,
    )

    await message.answer("Дані доставки успішно збережені!")
    
    move_to = dialog_manager.start_data.get("move_to")
    if move_to is not None:
        return await dialog_manager.start(move_to)

    await dialog_manager.switch_to(ShippingStates.show)


async def invalid_data_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error):
    await message.reply("Введено неправильні дані, повторіть ще раз")