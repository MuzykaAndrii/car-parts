from rest_framework.serializers import ModelSerializer

from user.api.serializers import UserSerializer
from telegram.models import Account


class CreateAccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
        )


class AccountSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Account
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "user",
        )