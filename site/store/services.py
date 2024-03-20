from datetime import datetime
from main.models import Part, PartUnit
from store.exceptions import CartNotFoundError, PartNotFoundError, UserNotOwnerOfOrderError
from store.models import Order


def get_user_cart(user_id: int) -> Order:
    try:
        return Order.objects.get(customer_id=user_id, status=Order.STATUSES.IN_CART)
    except Order.DoesNotExist:
        raise CartNotFoundError


def get_part_unit(user_id: int, part_unit_id: int) -> PartUnit:
    return PartUnit.objects.get(id=part_unit_id, order__customer_id=user_id)


def get_or_create_user_cart(user_id: int) -> Order:
    cart, is_created = Order.objects.get_or_create(customer_id=user_id, status=Order.STATUSES.IN_CART)
    return cart


def add_to_cart(cart_id: int, part_id: int, quantity: int) -> Part:
    try:
        part = Part.objects.get(pk=part_id)
    except Part.DoesNotExist:
        raise PartNotFoundError

    pu = PartUnit.objects.create(
        part=part,
        order_id=cart_id,
        quantity=quantity,
        buy_price=part.buy_price,
        sell_price=part.sell_price,
    )

    return part


def delete_from_cart(user_id: int, part_unit_id: int) -> None:
    try:
        part_unit = PartUnit.objects.select_related("order__customer").get(pk=part_unit_id)
    except PartUnit.DoesNotExist:
        raise PartNotFoundError
    
    if part_unit.order.customer.pk != user_id:
        raise UserNotOwnerOfOrderError
    
    part_unit.delete()


def clear_cart(user_id: int) -> None:
    try:
        Order.objects.get(customer_id=user_id, status=Order.STATUSES.IN_CART).delete()
    except Order.DoesNotExist:
        pass


def submit_user_order(user_id: int) -> Order:
    cart = get_user_cart(user_id)

    cart.status = Order.STATUSES.SUBMITTED
    cart.sold_at = datetime.now()
    cart.save()

    return cart


def get_user_orders(user_id: int) -> list[Order]:
    return Order.with_accepted_statuses.filter(customer_id=user_id).order_by("-sold_at")