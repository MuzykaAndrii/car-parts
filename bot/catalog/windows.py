import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Group, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog

from .actions import car_provider_clicked, get_car_producers
from .states import CatalogStates


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


catalog_dialog = Dialog(car_providers_window)