from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAdminUser

from main.api.serializers import PartUnitSerializer
from store.exceptions import CartNotFoundError, PartNotFoundError, UserNotOwnerOfOrderError
from store import services as store_services
from store.api.serializers import AddToCartSerializer, OrderSerializer


class UserCartEndpoint(APIView):
    permission_classes = [IsAdminUser | HasAPIKey]

    def get(self, request: HttpRequest, user_id: int):
        try:
            cart = store_services.get_user_cart(user_id)
        except CartNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(cart, many=False)
        return Response(serializer.data)

    def delete(self, request: HttpRequest, user_id: int):
        try:
            store_services.clear_cart(user_id)
        except CartNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CartProductsEndpoint(APIView):
    permission_classes = [IsAdminUser | HasAPIKey]

    def get(self, request: HttpRequest, user_id: int, part_unit_id: int):
        part_unit = store_services.get_part_unit(user_id, part_unit_id)
        serializer = PartUnitSerializer(part_unit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, user_id: int):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        part_id = serializer.validated_data.get("part_id")
        quantity = serializer.validated_data.get("quantity")

        try:
            cart = store_services.get_or_create_user_cart(user_id)
            part = store_services.add_to_cart(cart.pk, part_id, quantity)
        except (CartNotFoundError, PartNotFoundError):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: HttpRequest, user_id: int, part_unit_id: int):
        try:
            store_services.delete_from_cart(user_id, part_unit_id)
        except (UserNotOwnerOfOrderError, PartNotFoundError):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubmitOrderEndpoint(APIView):
    permission_classes = [IsAdminUser | HasAPIKey]

    def patch(self, request: HttpRequest, user_id: int):
        try:
            order = store_services.submit_user_order(user_id)
            serializer = OrderSerializer(order)
        except CartNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserOrdersEndpoint(APIView):
    permission_classes = [IsAdminUser | HasAPIKey]

    def get(self, request: HttpRequest, user_id: int):
        orders = store_services.get_user_orders(user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)