from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from components import backend_session as session


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


@router.message(Command("vendors"))
async def command_vendors_handler(message: Message) -> None:
    async with session().get("/api/car_producers/") as resp:
        car_vendors = await resp.json()
    
    msg = "\n".join(car["name"] for car in car_vendors)
    await message.answer(msg)