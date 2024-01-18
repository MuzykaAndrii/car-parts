from django.urls import include, path, re_path
from django.conf import settings
from main.admin import admin_site
from main.views import handler500 as h500
import re
from django.views.static import serve


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('main.urls', namespace='main')),
    path('stats/', include('statistic.urls', namespace='stats')),
    re_path( r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")), view=serve, kwargs = {'document_root':settings.STATIC_ROOT}),
    path('user/', include('user.urls', namespace='user')),
    path("garage/", include("garage.urls", namespace="garage")),
    path("store/", include("store.urls", namespace="store")),
]
if settings.DEBUG:
    urlpatterns.append(path('500/', h500))

handler500 = 'main.views.handler500'