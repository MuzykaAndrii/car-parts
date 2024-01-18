from django.urls import path

from store.views import AddToOrderView, ShowOrderView


app_name = 'store'

urlpatterns = [
    path("add_to_order/", AddToOrderView.as_view(), name="add_to_order"),
    path("cart/", ShowOrderView.as_view(), name="cart"),
]