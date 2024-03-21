from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from cart.states import CartStates
from cart.windows import cart_dialog


router = Router()
router.include_router(cart_dialog)

@router.message(Command("cart"))
async def command_cart_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(CartStates.cart_detail, mode=StartMode.RESET_STACK)