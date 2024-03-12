


from store.models import Order


def get_user_cart(user_id: int) -> Order | None:
    actual_order = Order.objects.filter(customer_id=user_id, status=Order.STATUSES.IN_CART).first()
    return actual_order


def get_or_create_user_cart(user_id: int) -> Order:
    cart, is_created = Order.objects.get_or_create(customer=user_id, status=Order.STATUSES.IN_CART)
    return cart