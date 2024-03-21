from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from core.admin import admin_site

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
    path("telegram/", include("telegram.urls", namespace="telegram")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)