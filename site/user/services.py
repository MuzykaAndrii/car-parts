import uuid

from django.contrib.auth.models import User

from user.models import ShippingAddress


def get_user_shipping_address(user_id: int) -> ShippingAddress | None:
    try:
        return ShippingAddress.objects.get(user_id=user_id)
    except ShippingAddress.DoesNotExist:
        return None


def create_random_user() -> User:
    return User.objects.create_user(
        username=uuid.uuid4(),
    )