from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Select

from .states import CatalogStates


async def start_catalog_dialog(event: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(
        CatalogStates.car_providers,
        mode=StartMode.NEW_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


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