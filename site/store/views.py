from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from store.exceptions import CartNotFoundError, PartNotFoundError, UserNotOwnerOfOrderError
from store.forms import AddToOrderForm, DeleteFromOrderForm
from auth.mixins import MyLoginRequiredMixin
from store import services as store_services
from user import services as user_services
from store import services as store_services



class AddToCartView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        form = AddToOrderForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Відбулась помилка, перевірте правильність введених даних")
            return redirect("main:car_producers_catalog")
        
        part_id = form.cleaned_data.get("part_id")
        quantity = form.cleaned_data.get("quantity")

        cart = store_services.get_or_create_user_cart(request.user.id)
        try:
            part = store_services.add_to_cart(cart.pk, part_id, quantity)
        except PartNotFoundError:
            raise Http404

        messages.success(request, f"Товар {part.name} доданий до корзини успішно")
        return redirect("main:parts_catalog", car_vin=part.belongs_to.pk)


class DeleteFromCartView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        form = DeleteFromOrderForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Помилка, товар не видалений")
            return redirect("store:cart")

        try:
            store_services.delete_from_cart(request.user.id, form.cleaned_data.get("part_unit_pk"))
        except PartNotFoundError:
            raise Http404
        except UserNotOwnerOfOrderError:
            raise PermissionDenied

        messages.success(request, "Товар успішно видалений з корзини")
        return redirect("store:cart")


class CartView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        try:
            cart = store_services.get_user_cart(request.user.id)
        except CartNotFoundError:
            cart = None 

        shipping = user_services.get_user_shipping_address(request.user.id)

        return render(request, "store/cart.html", {"cart": cart, "shipping": shipping})


class ClearCartView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        store_services.clear_cart(request.user.id)

        messages.success(request, "Кошик успішно очищено")
        return redirect("store:cart")


class SubmitOrderView(MyLoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        try:
            store_services.submit_user_order(request.user.id)
        except CartNotFoundError:
            raise Http404

        messages.success(request, "Замовлення успішно надійшло на обробку! Ми звяжемося з вами найближчим часом)")
        return redirect("main:index")


class OrdersHistoryView(MyLoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        orders = store_services.get_user_orders(request.user.id)
        
        return render(request, "store/orders_history.html", {"orders": orders})