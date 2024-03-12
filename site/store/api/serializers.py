from rest_framework.serializers import ModelSerializer, CharField, IntegerField, Serializer

from user.api.serializers import UserSerializer
from store.models import Order
from main.api.serializers import PartUnitSerializer


class OrderSerializer(ModelSerializer):
    customer = UserSerializer(many=False)
    status = CharField(source="get_status_display")
    products = PartUnitSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "sold_at",
            "total",
            "total_quantity",
            "products",
            "customer",
        )


class AddToCartSerializer(Serializer):
    user_id = IntegerField()
    part_id = IntegerField()
    quantity = IntegerField()


class DeleteFromCartSerializer(Serializer):
    user_id = IntegerField()
    part_unit_id = IntegerField()