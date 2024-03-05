import operator

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog

from backend.schemas import CarProducerSchema
from components import backend_service


class CatalogStates(StatesGroup):
    car_providers = State()
    cars_list = State()
    car_parts = State()


async def get_car_producers(dialog_manager: DialogManager, **kwargs) -> list[CarProducerSchema]:
    car_providers = await backend_service().get_car_producers()
    return {"car_providers": car_providers}


async def car_provider_clicked(callback: CallbackQuery, button: Button, manager: DialogManager, item_id: int):
    await manager.next()


car_providers_window = Window(
    Const("Оберіть марку авто ⚙️ 🔧"),
    Group(
        Select(
            Format("{item.name}"),
            id="car_provider_select",
            item_id_getter=operator.attrgetter("id"),
            items="car_providers",
            on_click=car_provider_clicked,
        ),
        id="car_providers_group",
        width=3,
    ),
    Cancel(),
    state=CatalogStates.car_providers,
    getter=get_car_producers,
)

router = Router()
dialog = Dialog(car_providers_window)
router.include_router(dialog)

@router.message(Command("catalog"))
async def command_catalog_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(CatalogStates.car_providers)