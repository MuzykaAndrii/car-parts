from django.urls import path

from store.api import views


app_name = "api"

urlpatterns = [
    path("users/<int:user_id>/cart", views.UserCartEndpoint.as_view(), name="user_cart"),

    path("users/<int:user_id>/cart/products", views.CartProductsEndpoint.as_view(), name="cart_products"),
    path("users/<int:user_id>/cart/products/<int:part_unit_id>", views.CartProductsEndpoint.as_view(), name="cart_product_detail"),

    path("users/<int:user_id>/order/submit", views.SubmitOrderEndpoint.as_view(), name="submit_order"),
    path("users/<int:user_id>/orders", views.UserOrdersEndpoint.as_view(), name="user_orders"),
]
