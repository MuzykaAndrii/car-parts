from django.http import HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from store import services as store_services
from store.api.serializers import OrderSerializer


class CartByUserView(APIView):
    def get(self, request: HttpRequest, user_id: int):
        cart = store_services.get_actual_user_order(user_id)

        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(cart, many=False)
        return Response(serializer.data)