"""
Core data models for ESG ingestion and analyst review.

RawDataRecord: immutable snapshot of uploaded data.
NormalizedEmissionRecord: unified schema for analyst review workflow.
"""
import hashlib
import json

from django.db import models

from tenants.models import Tenant


class SourceType(models.TextChoices):
    SAP = 'SAP', 'SAP'
    UTILITY = 'UTILITY', 'Utility'
    TRAVEL = 'TRAVEL', 'Travel'


class RecordStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class Scope(models.TextChoices):
    SCOPE_1 = 'SCOPE_1', 'Scope 1 (fuel)'
    SCOPE_2 = 'SCOPE_2', 'Scope 2 (electricity)'
    SCOPE_3 = 'SCOPE_3', 'Scope 3 (travel & procurement)'


class QualityFlag(models.TextChoices):
    MISSING_FIELD = 'MISSING_FIELD', 'Missing field'
    INVALID_UNIT = 'INVALID_UNIT', 'Invalid unit'
    SUSPICIOUS_VALUE = 'SUSPICIOUS_VALUE', 'Suspicious value'


class PlantCodeMapping(models.Model):
    """SAP plant code lookup per tenant."""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='plant_mappings')
    sap_code = models.CharField(max_length=32, db_index=True)
    display_name = models.CharField(max_length=255)
    region = models.CharField(max_length=64, blank=True)

    class Meta:
        unique_together = [('tenant', 'sap_code')]

    def __str__(self):
        return f'{self.sap_code} -> {self.display_name}'


class AirportDistance(models.Model):
    """IATA pair distances for travel normalization (km)."""

    from_iata = models.CharField(max_length=3, db_index=True)
    to_iata = models.CharField(max_length=3, db_index=True)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = [('from_iata', 'to_iata')]

    def __str__(self):
        return f'{self.from_iata}-{self.to_iata}: {self.distance_km} km'


class RawDataRecord(models.Model):
    """
    Immutable storage of ingested data exactly as received.
    Updates are blocked after creation to preserve audit trail.
    """

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='raw_records')
    source_type = models.CharField(max_length=16, choices=SourceType.choices)
    payload = models.JSONField(help_text='Parsed rows/JSON as received')
    filename = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=128, blank=True)
    checksum = models.CharField(max_length=64, blank=True)
    ingested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ingested_at']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError('RawDataRecord is immutable and cannot be updated')
        if not self.checksum and self.payload:
            raw = json.dumps(self.payload, sort_keys=True, default=str)
            self.checksum = hashlib.sha256(raw.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Raw {self.source_type} #{self.pk} ({self.tenant.client_id})'


class NormalizedEmissionRecord(models.Model):
    """
    Main emissions table — normalized quantities, scope, review workflow.
    Links back to RawDataRecord for raw -> normalized traceability.
    """

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='emission_records')
    raw_record = models.ForeignKey(
        RawDataRecord,
        on_delete=models.CASCADE,
        related_name='normalized_rows',
    )
    source_type = models.CharField(max_length=16, choices=SourceType.choices)
    status = models.CharField(
        max_length=16,
        choices=RecordStatus.choices,
        default=RecordStatus.PENDING,
        db_index=True,
    )
    scope = models.CharField(max_length=16, choices=Scope.choices, db_index=True)

    activity_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    quantity_raw = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    unit_raw = models.CharField(max_length=32, blank=True)
    quantity_normalized = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    unit_normalized = models.CharField(max_length=32, blank=True)

    emission_factor = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    co2e_kg = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)

    quality_flags = models.JSONField(default=list, help_text='List of QualityFlag values')
    normalized_payload = models.JSONField(default=dict, help_text='Unified schema snapshot')
    source_row_index = models.PositiveIntegerField(default=0, help_text='Index in raw payload rows')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.CharField(max_length=128, blank=True)
    review_notes = models.TextField(blank=True)
    edited_flag = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.source_type} #{self.pk} [{self.status}]'
