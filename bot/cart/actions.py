from typing import Literal

from aiogram_dialog import DialogManager
from aiogram.types import User

from backend.schemas import CartSchema
from components import backend_service


async def get_user_cart(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict[Literal["cart"], CartSchema | None]:
    account = await backend_service().get_account(event_from_user.id)
    cart = await backend_service().get_user_cart(account.user.id)

    return {"cart": cart}