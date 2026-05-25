from django.contrib import admin
from .models import (
    AirportDistance,
    NormalizedEmissionRecord,
    PlantCodeMapping,
    RawDataRecord,
)


@admin.register(RawDataRecord)
class RawDataRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'source_type', 'filename', 'ingested_at')
    readonly_fields = ('tenant', 'source_type', 'payload', 'filename', 'checksum', 'ingested_at')


@admin.register(NormalizedEmissionRecord)
class NormalizedEmissionRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'source_type', 'scope', 'status', 'activity_date')
    list_filter = ('status', 'source_type', 'scope')


@admin.register(PlantCodeMapping)
class PlantCodeMappingAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'sap_code', 'display_name', 'region')


@admin.register(AirportDistance)
class AirportDistanceAdmin(admin.ModelAdmin):
    list_display = ('from_iata', 'to_iata', 'distance_km')
