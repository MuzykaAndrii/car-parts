from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select

from orders.states import OrderStates
from shipping.states import ShippingStates
from catalog.states import CatalogStates
from components import backend_service
from .states import CartStates


async def clear_cart_clicked(event: CallbackQuery, widget: Button, manager: DialogManager):
    account = await backend_service().get_account(event.from_user.id)
    await backend_service().clear_cart(account.user.id)

    await manager.switch_to(CartStates.cart_cleared)


async def cart_product_clicked(callback: CallbackQuery, button: Select, manager: DialogManager, item_id: str):
    context = manager.current_context()
    context.dialog_data.update(product_id=item_id)

    await manager.switch_to(CartStates.manage_product)


async def delete_cart_product_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    context = manager.current_context()
    product_id = context.dialog_data.get("product_id")

    account = await backend_service().get_account(callback.from_user.id)
    is_deleted = await backend_service().delete_cart_product(account.user.id, product_id)

    context.dialog_data.update(is_deleted=is_deleted)
    await manager.switch_to(CartStates.product_deleted)


async def checkout_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    account = await backend_service().get_account(callback.from_user.id)
    cart = await backend_service().get_user_cart(account.user.id)
    shipping = await backend_service().get_user_shipping(account.user.id)

    if not cart:
        await manager.event.answer("Спочатку додайте товари в корзину")
        return await manager.start(CatalogStates.car_providers)
    
    if not shipping:
        return await manager.start(ShippingStates.show, data={"move_to": OrderStates.checkout})
    
    return await manager.start(OrderStates.checkout, data={"cart": cart, "shipping": shipping})