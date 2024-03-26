from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.admin import admin_site
from store.models import Order
from user.models import ShippingAddress


class OrdersInline(admin.TabularInline):
    model = Order
    extra = 0
    verbose_name = "Замовлення"
    verbose_name_plural = "Замовлення"
    fields = ("pk", "status", "sold_at")
    readonly_fields = ("pk", "sold_at")
    show_change_link = True


class ShippingInline(admin.StackedInline):
    model = ShippingAddress
    verbose_name = "Адреса доставки"
    verbose_name_plural = "Адреси доставки"


UserAdmin.inlines += (ShippingInline, OrdersInline)
UserAdmin.fieldsets = (
    (None, {"fields": ("username", "password")}),
    (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
)
admin_site.register(User, UserAdmin)