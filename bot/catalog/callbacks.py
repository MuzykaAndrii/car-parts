from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Select, ManagedCounter, Button


from components import backend_service
from .states import CatalogStates


async def car_provider_clicked(callback: CallbackQuery, button: Select, manager: DialogManager, item_id: int) -> None:
    context = manager.current_context()
    context.dialog_data.update(producer_id=item_id)
    await manager.switch_to(CatalogStates.cars_list)


async def car_model_clicked(callback: CallbackQuery, button: Select, manager: DialogManager, item_id: str) -> None:
    context = manager.current_context()
    context.dialog_data.update(car_vin=item_id)
    await manager.switch_to(CatalogStates.car_parts)


async def part_clicked(callback: CallbackQuery, button: Select, manager: DialogManager, item_id: str) -> None:
    context = manager.current_context()
    context.dialog_data.update(part_id=item_id)
    await manager.switch_to(CatalogStates.part_item)


async def amount_entered(event: CallbackQuery, widget: ManagedCounter, manager: DialogManager):
    context = manager.current_context()

    quantity = int(widget.get_value())
    part_id = context.dialog_data.get("part_id")

    account = await backend_service().get_account(event.from_user.id)
    await backend_service().add_to_cart(account.user.id, part_id, quantity)

    await manager.switch_to(CatalogStates.added)