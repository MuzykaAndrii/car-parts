from typing import Literal

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from backend.schemas import CarProducerSchema, CarSchema
from components import backend_service
from .states import CatalogStates



async def get_car_producers(dialog_manager: DialogManager, **kwargs) -> dict[Literal["car_providers"], list[CarProducerSchema]]:
    car_providers = await backend_service().get_car_producers()
    return {"car_providers": car_providers}


async def get_cars(dialog_manager: DialogManager, **kwargs) -> dict[Literal["cars"], list[CarSchema]]:
    context = dialog_manager.current_context()
    producer_id = context.dialog_data.get("producer_id")
    if not producer_id:
        await dialog_manager.event.answer('Please, select category first')
        await dialog_manager.switch_to(CatalogStates.car_providers)
        return

    cars = await backend_service().get_cars(producer_id)
    return {"cars": cars}


async def car_provider_clicked(callback: CallbackQuery, button: Select, manager: DialogManager, item_id: int) -> None:
    context = manager.current_context()
    context.dialog_data.update(producer_id=item_id)
    await manager.switch_to(CatalogStates.cars_list)


async def car_model_clicked(callback: CallbackQuery, button: Select, manager: DialogManager, item_id: str) -> None:
    context = manager.current_context()
    context.dialog_data.update(car_vin=item_id)
    await manager.switch_to(CatalogStates.car_parts)