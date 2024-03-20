from typing import Literal

from aiogram_dialog import DialogManager
from aiogram.types import User

from backend.schemas import CartSchema, PartUnitSchema
from components import backend_service


async def get_user_cart(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict[Literal["cart"], CartSchema | None]:
    account = await backend_service().get_account(event_from_user.id)
    cart = await backend_service().get_user_cart(account.user.id)

    return {"cart": cart}


async def get_cart_item_details(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict[Literal["product"], PartUnitSchema | None]:
    context = dialog_manager.current_context()
    product_id = context.dialog_data.get("product_id")

    account = await backend_service().get_account(event_from_user.id)
    product = await backend_service().get_cart_product(account.user.id, product_id)

    return {"product": product}