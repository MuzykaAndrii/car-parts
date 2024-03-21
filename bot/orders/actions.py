from aiogram.types import User
from aiogram_dialog import DialogManager

from components import backend_service


async def get_checkout_data(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    if dialog_manager.start_data:
        cart = dialog_manager.start_data.get("cart")
        shipping = dialog_manager.start_data.get("shipping")
    else:
        account = await backend_service().get_account(event_from_user.id)
        cart = await backend_service().get_user_cart(account.user.id)
        shipping = await backend_service().get_user_shipping(account.user.id)
    
    return {"shipping": shipping, "cart": cart}