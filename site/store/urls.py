from django.urls import include, path

from store.views import AddToCartView, ClearCartView, DeleteFromCartView, OrdersHistoryView, CartView, SubmitOrderView


app_name = 'store'

urlpatterns = [
    path("add_to_order/", AddToCartView.as_view(), name="add_to_order"),
    path("cart/", CartView.as_view(), name="cart"),
    path("delete_from_order/", DeleteFromCartView.as_view(), name="delete_from_order"),
    path("clear_order/", ClearCartView.as_view(), name="clear_order"),
    path("submit_order/", SubmitOrderView.as_view(), name="submit_order"),
    path("history/", OrdersHistoryView.as_view(), name="orders_history"),

    path("api/", include("store.api.urls", namespace="api")),
]