from typing import Literal

from aiogram_dialog import DialogManager

from backend.schemas import CarPartSchema, CarProducerSchema, CarSchema
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


async def get_parts(dialog_manager: DialogManager, **kwargs) -> dict[Literal["parts"], list[CarPartSchema]]:
    context = dialog_manager.current_context()
    producer_id = context.dialog_data.get("producer_id")
    car_vin = context.dialog_data.get("car_vin")

    if not producer_id or not car_vin:
        await dialog_manager.event.answer('Please, select category first')
        await dialog_manager.switch_to(CatalogStates.car_providers)
        return
    
    parts = await backend_service().get_parts(producer_id, car_vin)

    return {"parts": parts}


async def get_part(dialog_manager: DialogManager, **kwargs) -> dict[Literal["part"], CarPartSchema]:
    context = dialog_manager.current_context()
    producer_id = context.dialog_data.get("producer_id")
    car_vin = context.dialog_data.get("car_vin")
    part_id = context.dialog_data.get("part_id")

    part = await backend_service().get_part(producer_id, car_vin, part_id)
    return {"part": part}