from aiogram_dialog import DialogManager

from components import backend_service
from .states import ShippingStates


async def save_shipping_data(user_id: int, manager: DialogManager, **fields):
    account = await backend_service().get_account(user_id)
    await backend_service().create_user_shipping(
        user_id=account.user.id,
        **fields,
    )

    start_data = manager.start_data
    if start_data and start_data.get("move_to"):
        return await manager.start(start_data.get("move_to"))

    await manager.switch_to(ShippingStates.show)
