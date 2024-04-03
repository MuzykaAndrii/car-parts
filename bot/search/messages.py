from aiogram import F, Router
from aiogram.types import Message


router = Router()


@router.message(F.text)
async def search_products_handler(message: Message):
    await message.answer(message.text)