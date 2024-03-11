from django.urls import path

from store.api.views import CartView


app_name = "api"

urlpatterns = [
    path("cart/<int:user_id>", CartView.as_view(), name="get_cart"),
]
