


from store.models import Order


def get_actual_user_order(user_id: int) -> Order | None:
    actual_order = Order.objects.filter(customer_id=user_id, status=Order.STATUSES.IN_CART).first()
    return actual_order