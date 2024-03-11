from rest_framework.serializers import ModelSerializer, CharField

from user.api.serializers import UserSerializer
from store.models import Order


class OrderSerializer(ModelSerializer):
    customer = UserSerializer(many=False)
    status = CharField(source="get_status_display")

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "status",
            "sold_at",
            "total",
            "total_quantity",
        )