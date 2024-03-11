from django.http import HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from store import services as store_services
from store.api.serializers import OrderSerializer


class CartView(APIView):
    def get(self, request: HttpRequest, user_id: int):
        print(user_id)
        cart = store_services.get_actual_user_order(user_id)
        print(cart)
        serializer = OrderSerializer(cart, many=False)

        return Response(serializer.data)