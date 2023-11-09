from django.urls import path

from .views import register_user
from .views import login_user
from .views import logout_user


app_name = "user"

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]
