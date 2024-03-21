from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from components import backend_service 
from .states import OrderStates


async def submit_order_clicked(callback: CallbackQuery, widget: Button, manager: DialogManager):
    account = await backend_service().get_account(callback.from_user.id)
    await backend_service().submit_user_order(account.user.id)

    await manager.switch_to(OrderStates.submitted)