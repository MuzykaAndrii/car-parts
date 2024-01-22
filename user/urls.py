from django.urls import path

from user.views import ShippingView


app_name = "user"

urlpatterns = [
    path("settings/", ShippingView.as_view(), name="shipping"),
]
