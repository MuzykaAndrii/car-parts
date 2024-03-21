from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode


from .windows import shipping_dialog
from .states import ShippingStates


router = Router()
router.include_router(shipping_dialog)


@router.message(Command("shipping"))
async def command_shipping_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(ShippingStates.show, mode=StartMode.RESET_STACK)