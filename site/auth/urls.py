from django.urls import path

from .views import UserLoginView, UserLogoutView, UserRegisterView


app_name = "auth"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
