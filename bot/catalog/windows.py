import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Select, Back, Button, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog import Dialog

from .states import CatalogStates
from . import actions, callbacks, messages


car_providers_window = Window(
    Const(messages.car_provider_title),
    ScrollingGroup(
        Select(
            Format(messages.car_provider_item),
            id="car_provider_select",
            item_id_getter=operator.attrgetter("id"),
            items="car_providers",
            on_click=callbacks.car_provider_clicked,
        ),
        id="car_providers_group",
        hide_on_single_page=True,
        width=4,
        height=4,
    ),
    Cancel(Const(messages.car_providers_cancel)),
    state=CatalogStates.car_providers,
    getter=actions.get_car_producers,
)


cars_list_window = Window(
    Const(messages.cars_list_title),
    ScrollingGroup(
        Select(
            Format(messages.cars_list_item),
            id="car_select",
            item_id_getter=operator.attrgetter("vin"),
            items="cars",
            on_click=callbacks.car_model_clicked,
        ),
        id="cars_list_group",
        hide_on_single_page=True,
        width=1,
        height=6,
    ),
    Back(Const(messages.cars_list_back)),
    state=CatalogStates.cars_list,
    getter=actions.get_cars,
)


parts_list_window = Window(
    Const(messages.parts_list_title),
    ScrollingGroup(
        Select(
            Format(messages.parts_list_item),
            id="part_select",
            item_id_getter=operator.attrgetter("id"),
            items="parts",
            on_click=callbacks.part_clicked,
        ),
        id="parts_list_group",
        hide_on_single_page=True,
        width=2,
        height=6,
    ),
    Back(Const(messages.parts_list_back)),
    state=CatalogStates.car_parts,
    getter=actions.get_parts,
)


part_item_window = Window(
    Jinja(messages.part_item_template),
    Button(
        Const(messages.add_to_cart),
        id="add_to_cart",
        on_click=...
    ),
    Back(Const(messages.part_item_back)),
    state=CatalogStates.part_item,
    parse_mode="HTML",
    getter=actions.get_part,
)


catalog_dialog = Dialog(
    car_providers_window,
    cars_list_window,
    parts_list_window,
    part_item_window,
)