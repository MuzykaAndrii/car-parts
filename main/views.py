from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response

from auth.mixins import AdminRequiredMixin

from .models import CarProducer, Part, Auto


class IndexPage(TemplateView):
    template_name='index.html'

class ScannerPage(AdminRequiredMixin, TemplateView):
    template_name='scanner.html'

class PartByScanner(APIView):
    def post(self, request):
        # TODO: add permission checking
        barcode = request.data.get('barcode')
        if not barcode: 
            return Response({'error' : True, 'msg' : 'Missing barcode value'})
        try:
            part = Part.objects.get(barcode=barcode)
        except ObjectDoesNotExist:
            return Response({'error' : True, 'msg' : 'No parts with this barcode.\nTry again'})
        except Exception as e:
            return Response({'error' : True, 'msg' : f'{e}'})
        else:
            return Response({'error' : False, 'msg' : 'Success', 'data' : part.id })

def handler500(request, template_name="status_pages/500.html"):
    response = render(request=request, template_name=template_name)
    response.status_code = 500
    return response


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

        return render(request, "main/parts_catalog.html", {"car": car})