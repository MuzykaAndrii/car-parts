from typing import Literal
from aiogram.types import User
from aiogram_dialog import DialogManager

from backend.schemas import ShippingSchema
from components import backend_service


async def get_user_shipping(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict[Literal["shipping"], ShippingSchema | None]:
    account = await backend_service().get_account(event_from_user.id)
    shipping = await backend_service().get_user_shipping(account.user.id)

    return {"shipping": shipping}
