from django.urls import path

from user.api.views import ShippingAddressEndpoint


app_name = "api"

urlpatterns = [
    path("<int:user_id>/shipping/", ShippingAddressEndpoint.as_view(), name="shipping"),
]
