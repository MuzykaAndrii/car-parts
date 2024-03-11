from django.urls import include, path

from user.views import ShippingView


app_name = "user"

urlpatterns = [
    path("shipping/", ShippingView.as_view(), name="shipping"),

    path("api/", include("user.api.urls", namespace="api")),
]
