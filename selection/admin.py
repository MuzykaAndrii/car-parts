from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet

from core.admin import admin_site
from selection.models import SelectionRequest, SelectionResponse


class SelectionResponseInline(admin.StackedInline):
    model = SelectionResponse
    verbose_name = "Підбір"
    extra = 1
    max_num = 1


# class HaveResponse(admin.SimpleListFilter):
#     title = "наявністю відповіді"
#     parameter_name = "have_response"

#     def lookups(self, request, model_admin):
#         return (
#             ("Yes", 'Підбір здійснений'),
#             ("No", 'Чекає підбору'),
#         )
    
#     def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
#         value = self.value()

#         match value:
#             case "No":
#                 return queryset.filter(response=None)
#             case "Yes" | _:
#                 return queryset


class SelectionRequestAdmin(admin.ModelAdmin):
    fields = ("id", "sender", "to_car", "text", "requested_at", "status")
    readonly_fields = ("id", "sender", "to_car", "text", "requested_at", "status")

    list_display = ("id", "__str__", "requested_at", "status")
    list_display_links = ("id", "__str__",)
    list_filter = ("status", "requested_at")

    inlines = [SelectionResponseInline]

    def has_add_permission(self, request, obj=None):
        return False


admin_site.register(SelectionRequest, SelectionRequestAdmin)
