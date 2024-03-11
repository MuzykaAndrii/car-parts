from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from components import backend_service


router = Router()

@router.message(Command("cart"))
async def command_cart_handler(message: Message) -> None:
    account = await backend_service().get_account(message.from_user.id)
    cart = await backend_service().get_cart_by_user(account.user.id)
    print(cart)