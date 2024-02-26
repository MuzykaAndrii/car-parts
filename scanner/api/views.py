from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Part



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