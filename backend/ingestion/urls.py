from django.urls import path

from .views import IngestSAPView, IngestTravelView, IngestUtilityView

urlpatterns = [
    path('ingest/sap/', IngestSAPView.as_view(), name='ingest-sap'),
    path('ingest/utility/', IngestUtilityView.as_view(), name='ingest-utility'),
    path('ingest/travel/', IngestTravelView.as_view(), name='ingest-travel'),
]
