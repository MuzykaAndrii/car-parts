from datetime import datetime

from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from main.models import Part, PartUnit

from store.forms import AddToOrderForm, DeleteFromOrderForm
from store import services as store_services
from store.models import Order
from auth.mixins import MyLoginRequiredMixin
from user import services as user_services
from store import services as store_services



class AddToCartView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        form = AddToOrderForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Відбулась помилка, перевірте правильність введених даних")
            return redirect("main:car_producers_catalog")
        
        cart = store_services.get_or_create_user_cart(request.user.id)
        part = get_object_or_404(Part, pk=form.cleaned_data.get("part_id"))
        PartUnit.objects.create(
            part=part,
            order=cart,
            quantity=form.cleaned_data.get("quantity"),
            buy_price=part.buy_price,
            sell_price=part.sell_price,
        )

        messages.success(request, f"Товар {part.name} доданий до корзини успішно")
        return redirect("main:parts_catalog", car_vin=part.belongs_to.pk)


class DeleteFromCartView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        form = DeleteFromOrderForm(request.POST)

        if not form.is_valid():
            return self.send_error(request)
        
        part_unit = get_object_or_404(
            PartUnit.objects.select_related("order__customer"),
            pk=form.cleaned_data.get("part_unit_pk")
        )

        if part_unit.order.customer != request.user:
            return self.send_error(request)
        
        part_unit.delete()

        messages.success(request, "Товар успішно видалений з корзини")
        return redirect("store:cart")

    def send_error(self, request):
        messages.error(request, "Помилка, товар не видалений")
        return redirect("store:cart")


class CartView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        cart = store_services.get_user_cart(request.user.id)
        shipping = user_services.get_user_shipping_address(request.user)

        return render(request, "store/cart.html", {"cart": cart, "shipping": shipping})


class ClearCartView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        get_object_or_404(
           Order.objects,
           customer=request.user,
           status=Order.STATUSES.IN_CART
        ).delete()

        messages.success(request, "Кошик успішно очищено")
        return redirect("store:cart")


class SubmitOrderView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
       order_to_submit = store_services.get_user_cart(request.user.id)
       if not order_to_submit:
           raise Http404

       order_to_submit.status = Order.STATUSES.SUBMITTED
       order_to_submit.sold_at = datetime.now()
       order_to_submit.save()

       messages.success(request, "Замовлення успішно надійшло на обробку! Ми звяжемося з вами найближчим часом)")
       return redirect("main:index")


class OrdersHistoryView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        orders = Order.with_accepted_statuses.filter(customer=request.user)
        
        return render(request, "store/orders_history.html", {"orders": orders})