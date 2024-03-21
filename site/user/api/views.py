from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from user import services as user_services
from user.api.serializers import ShippingAddressSerializer


class ShippingAddressEndpoint(APIView):
    def get(self, request: HttpRequest, user_id: int):
        shipping = user_services.get_user_shipping_address(user_id)

        if shipping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ShippingAddressSerializer(shipping, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request: HttpRequest, user_id: int):
        existing_shipping = user_services.get_user_shipping_address(user_id)
        if existing_shipping:
            return Response(status=status.HTTP_409_CONFLICT)

        request.data['user_id'] = user_id
        serializer = ShippingAddressSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request: HttpRequest, user_id: int):
        shipping = user_services.get_user_shipping_address(user_id)

        if shipping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ShippingAddressSerializer(shipping, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)