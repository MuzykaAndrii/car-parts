import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Url,
    ListGroup,
    Cancel,
    ScrollingGroup,
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog

from .states import SearchStates
from . import actions


searching_success = F["products"]
search_failed = ~searching_success


results_window = Window(
    Const("Результати пошуку:", when=searching_success),
    ScrollingGroup(
        ListGroup(
            Url(
                Format("{item.name} ({item.producer}) {item.belongs_to}"),
                Format("{item.part_url}"),
                id="search_url",
            ),
            id="part_select_search",
            item_id_getter=operator.attrgetter("id"),
            items="products",
        ),
        id="parts_search_group",
        hide_on_single_page=True,
        width=1,
        height=6,
        when=searching_success,
    ),

    Const("Пошук не дав результатів(", when=search_failed),

    Cancel(Const('Вийти')),

    state=SearchStates.view_results,
    getter=actions.search,
)


dialog = Dialog(
    results_window,
)