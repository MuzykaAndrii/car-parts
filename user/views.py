from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View


class SettingsView(View):
    def get(self, request: HttpRequest):
        # Show settings page
        pass

    def post(self, request: HttpRequest):
        # upd account data
        pass