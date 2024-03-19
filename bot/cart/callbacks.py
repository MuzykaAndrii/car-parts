from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd import ManagedCounter

from backend import services as backend_service
from .states import CartStates


async def add_to_cart_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    context = manager.current_context()
    part_id = context.dialog_data.get("part_id")

    await manager.start(CartStates.enter_amount, data={"part_id": part_id})


async def amount_entered(event: CallbackQuery, widget: ManagedCounter, manager: DialogManager):
    context = manager.current_context()

    quantity = int(widget.get_value())
    part_id = context.start_data.get("part_id")

    account = await backend_service.get_account(event.from_user.id)
    await backend_service.add_to_cart(account.user.id, part_id, quantity)

    await manager.switch_to(CartStates.cart_detail)


async def clear_cart_clicked(event: CallbackQuery, widget: Button, manager: DialogManager):
    account = await backend_service.get_account(event.from_user.id)
    await backend_service.clear_cart(account.user.id)

    await manager.switch_to(CartStates.cart_cleared)