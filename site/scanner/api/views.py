from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Part



class PartByScannerEndpoint(APIView):
    def post(self, request, format=None):
        # TODO: add permission checking
        barcode = request.data.get("barcode")
        if not barcode:
            return Response(status=400, data={'msg' : 'Missing barcode value'})
        try:
            part = Part.objects.get(barcode=barcode)
        except ObjectDoesNotExist:
            return Response(status=404, data={'msg' : 'No parts with this barcode.\nTry again'})
        except Exception as e:
            return Response(status=500, data={'msg' : f'{e}'})
        else:
            return Response(status=200, data={'msg' : 'Success', 'data' : part.id })