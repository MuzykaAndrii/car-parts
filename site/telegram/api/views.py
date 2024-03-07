from django.http import HttpRequest

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.services import create_random_user
from telegram.api.serializers import AccountSerializer


class AccountView(APIView):
    def post(self, request: HttpRequest):
        new_account = AccountSerializer(data=request.data)

        if not new_account.is_valid():
            return Response(new_account.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = create_random_user()
        new_account.save(user=user)
        return Response(new_account.data, status=status.HTTP_201_CREATED)