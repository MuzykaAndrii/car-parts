from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Case


def cart_is_present(data: dict, case: Case, manager: DialogManager) -> bool:
    cart = data.get("cart", None)

    if cart is None:
        return False
    
    if not cart.products:
        return False
    
    return True

def cart_is_not_present(data: dict, case: Case, manager: DialogManager) -> bool:
    return not cart_is_present(data, case, manager)