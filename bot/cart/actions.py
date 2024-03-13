from typing import Literal

from aiogram_dialog import DialogManager

from backend.schemas import CartSchema
from components import backend_service


async def get_user_cart(dialog_manager: DialogManager, **kwargs) -> dict[Literal["cart"], CartSchema | None]:
    user_id = dialog_manager.start_data.get("user_id")

    account = await backend_service().get_account(user_id)
    cart = await backend_service().get_user_cart(account.user.id)

    return {"cart": cart}