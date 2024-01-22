from django.urls import path

from user.views import ShippingView


app_name = "user"

urlpatterns = [
    path("shipping/", ShippingView.as_view(), name="shipping"),
]
