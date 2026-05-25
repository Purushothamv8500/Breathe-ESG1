from django.contrib import admin
from django.urls import include, path

from .views import root

urlpatterns = [
    path('', root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('ingestion.urls')),
    path('api/', include('records.urls')),
]
