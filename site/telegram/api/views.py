from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAdminUser

from telegram.models import Account
from user.services import create_random_user
from telegram.api.serializers import AccountSerializer, CreateAccountSerializer


class CreateAccountEndpoint(APIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    
    def post(self, request: HttpRequest):
        new_account = CreateAccountSerializer(data=request.data)

        if not new_account.is_valid():
            return Response(new_account.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = create_random_user()
        new_account.save(user=user)
        return Response(new_account.data, status=status.HTTP_201_CREATED)


class GetAccountEndpoint(APIView):
    permission_classes = [IsAdminUser | HasAPIKey]

    def get(self, request: HttpRequest, account_id: int):
        account = get_object_or_404(Account.objects, id=account_id)
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)