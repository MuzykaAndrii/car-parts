from django.urls import path

from store.api.views import AddToCartEndpoint, ClearCartEndpoint, DeleteFromCartEndpoint


app_name = "api"

urlpatterns = [
    path("cart/add", AddToCartEndpoint.as_view(), name="add_to_cart"),
    path("cart/delete-product", DeleteFromCartEndpoint.as_view(), name="delete_from_cart"),
    path("cart/clear", ClearCartEndpoint.as_view(), name="clear_cart"),
]
