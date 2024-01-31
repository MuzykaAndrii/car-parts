from django.contrib import admin

from core.admin import admin_site
from selection.models import SelectionRequest, SelectionResponse


class SelectionResponseInline(admin.StackedInline):
    model = SelectionResponse
    verbose_name = "Підбір"
    extra = 1
    max_num = 1


class SelectionRequestAdmin(admin.ModelAdmin):
    fields = ("id", "sender", "to_car", "text",)
    readonly_fields = ("id", )

    # inlines = [
    #     SelectionResponseInline
    # ]


admin_site.register(SelectionRequest, SelectionRequestAdmin)
