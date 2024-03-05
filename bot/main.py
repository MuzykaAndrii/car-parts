import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from config import settings
from base.handlers import router as base_router
from catalog.handlers import router as catalog_router
from components import backend_session
from sessions import close_session


async def on_shutdown():
    await close_session(backend_session())


async def main() -> None:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    setup_dialogs(dp)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(
        base_router,
        catalog_router
    )

    bot = Bot(settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main(), debug=settings.DEBUG)