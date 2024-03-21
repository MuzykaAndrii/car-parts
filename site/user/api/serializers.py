from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

from user.models import ShippingAddress

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields =(
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
        )


class ShippingAddressSerializer(ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = (
            "user_id",
            "first_name",
            "last_name",
            "phone_number",
            "region",
            "city",
            "office_number",
        )