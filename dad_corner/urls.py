from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('kitchen/', include('kitchen.urls', namespace='kitchen')),
    path('', include('headquarter.urls', namespace='headquarter')),
    path('account/', include('account.urls')),
    path('menu/', include('menu.urls', namespace='menu')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    