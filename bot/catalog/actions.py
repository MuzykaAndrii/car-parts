from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from backend.schemas import CarProducerSchema
from components import backend_service



async def get_car_producers(dialog_manager: DialogManager, **kwargs) -> list[CarProducerSchema]:
    car_providers = await backend_service().get_car_producers()
    return {"car_providers": car_providers}


async def car_provider_clicked(callback: CallbackQuery, button: Button, manager: DialogManager, item_id: int):
    await manager.next()