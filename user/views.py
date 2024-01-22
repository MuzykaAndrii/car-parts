from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from auth.mixins import MyLoginRequiredMixin

from user.forms import ShippingAddressForm
from user.models import ShippingAddress


class ShippingView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        shipping_address = self.get_user_shipping_address(request.user)
        form = ShippingAddressForm(instance=shipping_address)

        return render(request, 'user/shipping.html', {"form": form})

    def post(self, request: HttpRequest):
        shipping_address = self.get_user_shipping_address(request.user)
        form = ShippingAddressForm(instance=shipping_address, data=request.POST)

        if not form.is_valid():
            messages.error(request, "Помилка! Не правильно введені дані. Спробуйте будь-ласка ще раз.")
            return render(request, 'user/shipping.html', {"form": form})
        
        new_shipping_address: ShippingAddress = form.save(commit=False)
        new_shipping_address.user = request.user
        new_shipping_address.save()

        messages.success(request, "Дані доставки успішно оновлені!")
        return render(request, 'user/shipping.html', {"form": form})

    def get_user_shipping_address(self, user) -> ShippingAddress | None:
        try:
            return ShippingAddress.objects.get(user=user)
        except ShippingAddress.DoesNotExist:
            return None