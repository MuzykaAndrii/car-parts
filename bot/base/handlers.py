from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from components import backend_service


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await backend_service().create_account(
        id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )
    await message.answer(f"Hello, {message.from_user.full_name}!")