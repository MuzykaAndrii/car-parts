from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from auth.mixins import MyLoginRequiredMixin

from user.forms import ShippingAddressForm
from user.models import ShippingAddress


class ShippingView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        try:
            shipping_address_instance = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            shipping_address_instance = None

        shipping_form = ShippingAddressForm(instance=shipping_address_instance)

        return render(request, 'user/shipping.html', {"shipping_form": shipping_form})

    def post(self, request: HttpRequest):
        # upd account data
        pass