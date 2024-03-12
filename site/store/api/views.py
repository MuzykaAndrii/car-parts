from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from store.exceptions import CartNotFoundError, PartNotFoundError, UserNotOwnerOfOrderError
from store import services as store_services
from store.api.serializers import AddToCartSerializer, UserIdSerializer, DeleteFromCartSerializer, OrderSerializer


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


class DeleteFromCartEndpoint(APIView):
    def delete(self, request: HttpRequest):
        serializer = DeleteFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data.get("user_id")
        part_unit_id = serializer.validated_data.get("part_unit_id")

        try:
            store_services.delete_from_cart(user_id, part_unit_id)
        except UserNotOwnerOfOrderError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except PartNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClearCartEndpoint(APIView):
    def delete(self, request: HttpRequest):
        serializer = UserIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data.get("user_id")

        try:
            store_services.clear_cart(user_id)
        except CartNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubmitOrderEndpoint(APIView):
    def patch(self, request: HttpRequest):
        serializer = UserIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data.get("user_id")

        try:
            order = store_services.submit_user_order(user_id)
            serializer = OrderSerializer(order)
        except CartNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserOrdersEndpoint(APIView):
    def get(self, request: HttpRequest):
        serializer = UserIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data.get("user_id")

        orders = store_services.get_user_orders(user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)