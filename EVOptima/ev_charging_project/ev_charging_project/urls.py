# File: ev_charging_project/ev_charging_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('prediction.urls')),
    path('visualization/', include('visualization.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)