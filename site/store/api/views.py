from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from store.exceptions import CartNotFoundError, PartNotFoundError
from store import services as store_services
from store.api.serializers import AddToCartSerializer, OrderSerializer


class UserCartEndpoint(APIView):
    def get(self, request: HttpRequest, user_id: int):
        cart = store_services.get_user_cart(user_id)

        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(cart, many=False)
        return Response(serializer.data)


class AddToCartEndpoint(APIView):
    def post(self, request: HttpRequest):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data.get("user_id")
        part_id = serializer.validated_data.get("part_id")
        quantity = serializer.validated_data.get("quantity")

        try:
            cart = store_services.get_or_create_user_cart(user_id)
            part = store_services.add_to_cart(cart.pk, part_id, quantity)
        except (CartNotFoundError, PartNotFoundError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_201_CREATED)