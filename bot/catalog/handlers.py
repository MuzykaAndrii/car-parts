from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from .states import CatalogStates
from .windows import catalog_dialog


router = Router()
router.include_router(catalog_dialog)

@router.message(Command("catalog"))
async def command_catalog_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(CatalogStates.car_providers)