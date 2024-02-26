from auth.mixins import AdminRequiredMixin
from django.views.generic import TemplateView



class ScannerPage(AdminRequiredMixin, TemplateView):
    template_name='scanner/scanner.html'