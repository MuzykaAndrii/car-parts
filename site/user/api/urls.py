from django.urls import path

from store.api.views import CartByUserView


app_name = "api"

urlpatterns = [
    path("<int:user_id>/cart", CartByUserView.as_view(), name="cart_by_user"),
]
