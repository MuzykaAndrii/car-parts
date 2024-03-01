from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View

from .forms import UserRegisterForm, UserLoginForm


class UserRegisterView(View):
    def post(self, request: HttpRequest):
        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Registration error")
            return render(request, "auth/register.html", {"form": form})

        form.save()
        messages.success(request, "User registration successful")
        return redirect("auth:login")

    def get(self, request: HttpRequest):
        form = UserRegisterForm()
        return render(request, "auth/register.html", {"form": form})


class UserLoginView(View):
    def get(self, request: HttpRequest):
        form = UserLoginForm()
        return render(request, "auth/login.html", {"form": form})

    def post(self, request: HttpRequest):
        form = UserLoginForm(data=request.POST)

        if not form.is_valid():
            return render(request, "auth/login.html", {"form": form})
        
        user = form.get_user()
        login(request, user)
        messages.success(request, f"{user.username} successfully logged in.")
        return redirect("main:index")


class UserLogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        messages.success(request, "Successfully logged out.")
        return redirect("auth:login")
