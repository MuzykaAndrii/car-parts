from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpRequest


from .models import CarProducer, Part, Auto, PartProducer


class IndexPage(TemplateView):
    template_name='index.html'


class CarProducerCatalog(View):
    def get(self, request: HttpRequest):
        car_producers = CarProducer.objects.all().order_by("name")
        return render(request, "main/car_producers_catalog.html", {"car_producers": car_producers})


class CarCatalog(View):
    def get(self, request: HttpRequest, car_producer: str):
        cars = Auto.objects.filter(producer__name=car_producer)
        return render(request, "main/car_catalog.html", {"cars": cars})


class PartsCatalog(View):
    def get(self, request: HttpRequest, car_vin: str):
        car = get_object_or_404(Auto, vin=car_vin)
        parts = Part.objects.filter(belongs_to=car)

        title = f"Запчастини до: {car.name}"
        return render(request, "main/parts_catalog.html", {"parts": parts, "title": title})


class PartDetail(View):
    def get(self, request: HttpRequest, car_vin: str, part_id: int):
        part = get_object_or_404(Part.objects.select_related("producer", "belongs_to__producer"), pk=part_id, belongs_to_id=car_vin)

        return render(request, "main/part_detail.html", {"part": part})


class PartProducerView(View):
    def get(self, request: HttpRequest, pk: int):
        producer = get_object_or_404(PartProducer, pk=pk)
        return render(request, "main/part_producer.html", {"producer": producer})


class PartProducersListView(View):
    def get(self, request: HttpRequest):
        producers = PartProducer.objects.all()
        return render(request, "main/part_producers_catalog.html", {"producers": producers})