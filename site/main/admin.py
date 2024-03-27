from django.contrib import admin

from .models import CarProducer, Auto, Part, PartProducer, PartUnit


class PartInline(admin.TabularInline):
    model = Part
    extra = 1

class AutoPage(admin.ModelAdmin):
    search_fields = ['vin', 'model']
    exclude = ("owners",)
    inlines = [
        PartInline,
    ]

class PartUnitInline(admin.TabularInline):
    model = PartUnit
    extra = 1
    fields = ['buy_price', 'sell_price',]

class PartPage(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['name', 'articul', 'belongs_to__model', 'belongs_to__producer__name']
    inlines = [
        PartUnitInline,
    ]


class PartProducerAdmin(admin.ModelAdmin):
    model = PartProducer




admin.site.register(CarProducer)
admin.site.register(Part, PartPage)
admin.site.register(Auto, AutoPage)
admin.site.register(PartProducer, PartProducerAdmin)