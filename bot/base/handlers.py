from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from components import backend_service


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


@router.message(Command("catalog"))
async def command_catalog_handler(message: Message) -> None:
    car_producers = await backend_service().get_car_producers()
    msg = "\n".join(producer.name for producer in car_producers)
    await message.answer(msg)