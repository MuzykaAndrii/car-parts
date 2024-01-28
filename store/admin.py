from django.contrib import admin

from core.admin import admin_site
from main.models import PartUnit
from store.models import Order


class PartUnitInline(admin.TabularInline):
    model = PartUnit
    extra = 0
    verbose_name = "Товар"
    verbose_name_plural = "Товари"


class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "__str__", "sold_at", "status")
    list_display_links = ("pk", "__str__")
    list_editable = ("status", )
    radio_fields = {"status": admin.VERTICAL}
    list_filter = ("status", "sold_at")

    search_fields = ("pk", )
    fields = ("id", "sold_at", "customer", "status")
    readonly_fields = ("id", "sold_at")

    date_hierarchy = "sold_at"
    ordering = ("-sold_at",)

    inlines = (
        PartUnitInline,
    )


admin_site.register(Order, OrderAdmin)
