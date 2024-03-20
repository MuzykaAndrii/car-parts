from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from components import backend_service
from .states import CartStates


async def clear_cart_clicked(event: CallbackQuery, widget: Button, manager: DialogManager):
    account = await backend_service().get_account(event.from_user.id)
    await backend_service().clear_cart(account.user.id)

    await manager.switch_to(CartStates.cart_cleared)