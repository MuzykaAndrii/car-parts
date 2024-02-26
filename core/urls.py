from django.urls import include, path
from django.conf import settings

from main.admin import admin_site
from main.views import handler500 as h500


urlpatterns = [
    path('admin/', admin_site.urls),
    path('auth/', include('auth.urls', namespace='auth')),
    path('', include('main.urls', namespace='main')),
    path('scanner/', include('scanner.urls', namespace='scanner')),
    path('stats/', include('statistic.urls', namespace='stats')),
    path('user/', include('user.urls', namespace='user')),
    path("garage/", include("garage.urls", namespace="garage")),
    path("store/", include("store.urls", namespace="store")),
    path("selection/", include("selection.urls", namespace="selection")),
]

if settings.DEBUG:
    urlpatterns.append(path('500/', h500))

handler500 = 'main.views.handler500'