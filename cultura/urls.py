from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('editais.urls')),
    path('', include('mapeamento_cultural.urls')),
    path('', include('qr_code.urls', namespace='qr_code')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
