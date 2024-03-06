import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Group, Select, Back, Button
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog import Dialog

from .actions import car_model_clicked, car_provider_clicked, get_car_producers, get_cars, get_part, get_parts, part_clicked
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
        width=4,
    ),
    Cancel(Const("Вийти")),
    state=CatalogStates.car_providers,
    getter=get_car_producers,
)


cars_list_window = Window(
    Const("Оберіть модель авто 🚗 🚕"),
    Group(
        Select(
            Format("📃: {item.model} 🗓️: {item.year_of_production} ⚙️: {item.engine_volume} 🛢️: {item.fuel}"),
            id="car_select",
            item_id_getter=operator.attrgetter("vin"),
            items="cars",
            on_click=car_model_clicked,
        ),
        id="cars_list_group",
        width=1,
    ),
    Back(Const("↩️ Обрати іншу марку")),
    state=CatalogStates.cars_list,
    getter=get_cars,
)


parts_list_window = Window(
    Const("Оберіть товар 🛞 🔧"),
    Group(
        Select(
            Format("{item.name} ®️: {item.producer}"),
            id="part_select",
            item_id_getter=operator.attrgetter("id"),
            items="parts",
            on_click=part_clicked,
        ),
        id="parts_list_group",
        width=2,
    ),
    Back(Const("↩️ Обрати іншу модель")),
    state=CatalogStates.car_parts,
    getter=get_parts,
)


part_item_window = Window(
    Jinja("""
    🔹 <b>Товар:</b> {{part.name}}
    🚗 <b>До авто:</b> {{part.belongs_to}}
    🏷️ <b>Артикул:</b> {{part.articul}}
    🏭 <b>Виробник:</b> {{part.producer}}
    💰 <b>Ціна:</b> {{part.sell_price}}
    """),
    Button(
        Const("🛒 Додати в корзину"),
        id="add_to_cart",
        on_click=...
    ),
    Back(Const("↩️ Обрати іншу деталь")),
    state=CatalogStates.part_item,
    parse_mode="HTML",
    getter=get_part,
)


catalog_dialog = Dialog(
    car_providers_window,
    cars_list_window,
    parts_list_window,
    part_item_window,
)