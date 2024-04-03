from aiogram import F, Router
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .windows import dialog as search_dialog
from .states import SearchStates


router = Router()
router.include_router(search_dialog)


@router.message(F.text)
async def search_products_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SearchStates.view_results, mode=StartMode.RESET_STACK, data={"query": message.text})