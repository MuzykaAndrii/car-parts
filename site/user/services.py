import uuid

from django.contrib.auth.models import User

from user.models import ShippingAddress


def get_user_shipping_address(user: User) -> ShippingAddress | None:
    try:
        return ShippingAddress.objects.get(user=user)
    except ShippingAddress.DoesNotExist:
        return None


def create_random_user() -> User:
    return User.objects.create_user(
        username=uuid.uuid4(),
    )