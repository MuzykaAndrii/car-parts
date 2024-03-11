from django.urls import include, path

from store.views import AddToOrderView, ClearOrderView, DeleteFromOrderView, OrdersHistoryView, ShowOrderView, SubmitOrderView


app_name = 'store'

urlpatterns = [
    path("add_to_order/", AddToOrderView.as_view(), name="add_to_order"),
    path("cart/", ShowOrderView.as_view(), name="cart"),
    path("delete_from_order/", DeleteFromOrderView.as_view(), name="delete_from_order"),
    path("clear_order/", ClearOrderView.as_view(), name="clear_order"),
    path("submit_order/", SubmitOrderView.as_view(), name="submit_order"),
    path("history/", OrdersHistoryView.as_view(), name="orders_history"),

    path("api/", include("store.api.urls", namespace="api")),
]