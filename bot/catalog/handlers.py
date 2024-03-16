from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager


from .windows import catalog_dialog
from .callbacks import start_catalog_dialog


router = Router()
router.include_router(catalog_dialog)

@router.message(Command("catalog"))
async def command_catalog_handler(message: Message, dialog_manager: DialogManager) -> None:
    await start_catalog_dialog(message, None, dialog_manager)