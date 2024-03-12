from django.urls import path

from store.api.views import AddToCartEndpoint


app_name = "api"

urlpatterns = [
    path("cart/add", AddToCartEndpoint.as_view(), name="add_to_cart"),
]
