import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Select,
    Back,
    Url,
    ScrollingGroup,
    Counter,
    Row,
    Start,
    SwitchTo
)
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog import Dialog


from cart.states import CartStates
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
    SwitchTo(Const(messages.add_to_cart), id="add_to_cart", state=CatalogStates.enter_amount),
    Url(Const("Дивитись на сайті"), Format("{part.part_url}"), id="part_url"),
    Back(Const(messages.part_item_back)),
    state=CatalogStates.part_item,
    parse_mode="HTML",
    getter=actions.get_part,
)


enter_product_amount_window = Window(
    Format("Введіть бажану кількість товару:"),
    Counter(
        id="amount_counter",
        default=1,
        min_value=1,
        max_value=50,
        plus=Const("➕"),
        minus=Const("➖"),
        text=Format("Додати {value:g}шт."),
        on_text_click=callbacks.amount_entered,
    ),
    Cancel(Const("Вийти")),
    state=CatalogStates.enter_amount,
)


product_added_window = Window(
    Const("Товар успішно доданий до корзини!"),
    Row(
        SwitchTo(Const("До каталогу"), id="to_catalog_btn", state=CatalogStates.car_providers),
        SwitchTo(Const("Обрати ще до цього авто"), id="to_products_btn", state=CatalogStates.car_parts),
    ),
    Start(Const("Корзина"), id="to_cart_btn", state=CartStates.cart_detail),
    Cancel(Const("❌ Вийти")),

    state=CatalogStates.added,
)


catalog_dialog = Dialog(
    car_providers_window,
    cars_list_window,
    parts_list_window,
    part_item_window,
    enter_product_amount_window,
    product_added_window,
)