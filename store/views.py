from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class AddToOrderView(View):
    def post(self, request: HttpRequest):
        ...