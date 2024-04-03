from typing import Literal

from aiogram_dialog import DialogManager

from backend.schemas import CarPartSchema
from components import backend_service


async def search(dialog_manager: DialogManager, **kwargs) -> dict[Literal["products"], list[CarPartSchema] | None]:
    search_query = dialog_manager.start_data.get("query")

    products = await backend_service().search_products(search_query)

    dialog_manager.dialog_data.update(products=products)
    return {"products": products}