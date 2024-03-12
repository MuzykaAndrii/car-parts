from django.http import HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count, Subquery, OuterRef

from rest_framework.response import Response
from rest_framework.views import APIView

from main.api.serializers import CarProducerSerializer, CarSerializer, PartSerializer
from main.models import Auto, CarProducer, Part
from store.models import Order


class CarProducersListEndpoint(APIView):
    def get(self, request: HttpRequest):
        car_producers = (
            CarProducer.objects
            .filter(cars__isnull=False, cars__parts__isnull=False)
            .annotate(
                sales_count=Count(
                    Subquery(
                        Order.objects.filter(
                            products__part__belongs_to__producer=OuterRef('pk'),
                            status=Order.STATUSES.RECEIVED
                        ).values('pk')
                    )
                )
            )
            .order_by("-sales_count", "name")
            .distinct()
        )

        serializer = CarProducerSerializer(car_producers, many=True)
        return Response(serializer.data)


class CarListEndpoint(APIView):
    def get(self, request: HttpRequest, producer_id: int):
        cars = get_list_or_404(Auto.objects.select_related("producer").distinct(), producer_id=producer_id, parts__isnull=False)

        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


class PartListEndpoint(APIView):
    def get(self, request: HttpRequest, car_producer_id: int, car_vin: str):
        parts = get_list_or_404(
            Part.objects.select_related("belongs_to").distinct(),
            belongs_to__producer_id=car_producer_id, belongs_to__vin=car_vin
        )

        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data)


class PartEndpoint(APIView):
    def get(self, request: HttpRequest, car_producer_id: int, car_vin: str, part_id: int):
        part = get_object_or_404(
            Part.objects.select_related("producer", "belongs_to"),
            belongs_to__producer_id=car_producer_id, belongs_to__vin=car_vin, id=part_id
        )

        serializer = PartSerializer(part)
        return Response(serializer.data)