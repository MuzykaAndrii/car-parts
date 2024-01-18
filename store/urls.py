from django.urls import path

from store.views import AddToOrderView


app_name = 'store'

urlpatterns = [
    path("add_to_order/", AddToOrderView.as_view(), name="add_to_order"),
]