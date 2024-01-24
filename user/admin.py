from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from core.admin import admin_site
from store.models import Order


class OrdersInline(admin.TabularInline):
    model = Order
    extra = 0
    verbose_name = "Замовлення"
    verbose_name_plural = "Замовлення"
    fields = ("pk", "status", "sold_at")
    readonly_fields = ("pk", "sold_at")
    show_change_link = True

UserAdmin.inlines += (OrdersInline, )
admin_site.register(User, UserAdmin)