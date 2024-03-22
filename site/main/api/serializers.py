from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from main.models import Auto, CarProducer, Part, PartUnit
from core import settings


class CarProducerSerializer(ModelSerializer):
    sales_count = SerializerMethodField()

    class Meta:
        model = CarProducer
        fields = ("id", "name", "sales_count")

    def get_sales_count(self, instance):
        return instance.sales_count


class CarSerializer(ModelSerializer):
    wheel_drive = CharField(source="get_wheel_drive_display")
    fuel = CharField(source="get_fuel_display")
    body = CharField(source="get_body_display")
    producer_name = CharField(source="producer.name")

    class Meta:
        model = Auto
        fields = (
            "vin",
            "model",
            "producer_id",
            "producer_name",
            "year_of_production",
            "engine_volume",
            "wheel_drive",
            "fuel",
            "body",
        )


class PartSerializer(ModelSerializer):
    producer = CharField(source="producer.name")
    belongs_to = CharField(source="belongs_to.name")
    producer_detail_url = SerializerMethodField()
    part_url = SerializerMethodField()

    def get_producer_detail_url(self, obj: Part) -> str:
        return settings.HOST_URL + obj.producer.get_absolute_url()
    
    def get_part_url(self, obj: Part):
        return settings.HOST_URL + obj.get_absolute_url()

    class Meta:
        model = Part
        fields = (
            "id",
            "name",
            "articul",
            "barcode",
            "sell_price",
            "producer",
            "belongs_to",
            "producer_detail_url",
            "part_url",
        )


class PartUnitSerializer(ModelSerializer):
    part = PartSerializer(many=False)

    class Meta:
        model = PartUnit
        fields = (
            "id",
            "quantity",
            "sell_price",
            "total_price",
            "part",
        )