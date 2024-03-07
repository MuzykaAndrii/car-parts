from django.contrib import admin

from core.admin import admin_site
from telegram.models import Account


class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user")
    readonly_fields = ("id", "username", "first_name", "last_name")

admin_site.register(Account, TelegramAccountAdmin)