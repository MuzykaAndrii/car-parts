from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from main.models import Part, PartUnit

from store.forms import AddToOrderForm, DeleteFromOrderForm
from store.models import Order
from auth.mixins import MyLoginRequiredMixin
from user import services as user_services



class AddToOrderView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        form = AddToOrderForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Відбулась помилка, перевірте правильність введених даних")
            return redirect("main:car_producers_catalog")
        
        actual_order = Order.objects.get_or_create(customer=request.user, status=Order.OrderStatus.CREATED)[0]
        part = get_object_or_404(Part, pk=form.cleaned_data.get("part_id"))
        PartUnit.objects.create(
            part=part,
            order=actual_order,
            quantity=form.cleaned_data.get("quantity"),
            buy_price=part.buy_price,
            sell_price=part.sell_price,
        )

        messages.success(request, "Товар доданий до корзини успішно")
        return redirect("main:parts_catalog", car_vin=part.belongs_to.pk)


class DeleteFromOrderView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):

        form = DeleteFromOrderForm(request.POST)

        if not form.is_valid():
            return self.send_error(request)
        
        part_unit = get_object_or_404(PartUnit, pk=form.cleaned_data.get("part_unit_pk"))

        if part_unit.order.customer != request.user:
            return self.send_error(request)
        
        part_unit.delete()

        messages.success(request, "Товар успішно видалений з корзини")
        return redirect("store:cart")

    def send_error(self, request):
        messages.error(request, "Помилка, товар не видалений")
        return redirect("store:cart")


class ShowOrderView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        actual_order = request.user.orders.get(status=Order.OrderStatus.CREATED)
        shipping = user_services.get_user_shipping_address(request.user)

        return render(request, "store/cart.html", {"cart": actual_order, "shipping": shipping})
