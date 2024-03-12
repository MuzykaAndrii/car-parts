from django.urls import path

from store.api.views import UserCartEndpoint


app_name = "api"

urlpatterns = [
    path("<int:user_id>/cart", UserCartEndpoint.as_view(), name="cart_by_user"),
]
