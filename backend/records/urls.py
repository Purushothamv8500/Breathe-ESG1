from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashboardView, RecordViewSet

router = DefaultRouter()
router.register(r'records', RecordViewSet, basename='records')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include(router.urls)),
]
