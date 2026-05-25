#!/usr/bin/env python
"""
Seed database with tenants, lookups, sample CSV ingestions, and one approved record.

Run from backend/: python scripts/seed.py
"""
import os
import sys
from pathlib import Path

import django

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decimal import Decimal  # noqa: E402

from django.core.files.uploadedfile import SimpleUploadedFile  # noqa: E402

from ingestion.parsers import parse_upload  # noqa: E402
from ingestion.service import ingest_rows  # noqa: E402
from records.models import (  # noqa: E402
    AirportDistance,
    NormalizedEmissionRecord,
    PlantCodeMapping,
    RecordStatus,
    SourceType,
)
from tenants.models import Tenant  # noqa: E402

SAMPLES_DIR = BACKEND_DIR.parent / 'samples'


def seed_tenants():
    acme, _ = Tenant.objects.get_or_create(client_id='acme', defaults={'name': 'Acme Corp'})
    globex, _ = Tenant.objects.get_or_create(client_id='globex', defaults={'name': 'Globex Industries'})
    return acme, globex


def seed_plant_mappings(tenant):
    mappings = [
        ('P001', 'North Manufacturing', 'US-Midwest'),
        ('P002', 'HQ Campus', 'US-East'),
        ('P003', 'West Distribution', 'US-West'),
        ('PLNT-S2', 'South Plant 2', 'US-South'),
    ]
    for code, name, region in mappings:
        PlantCodeMapping.objects.get_or_create(
            tenant=tenant, sap_code=code,
            defaults={'display_name': name, 'region': region},
        )


def seed_airports():
    pairs = [
        ('JFK', 'LAX', 3974),
        ('LHR', 'CDG', 344),
        ('ORD', 'LAX', 2800),
        ('SFO', 'NRT', 8270),
    ]
    for o, d, km in pairs:
        AirportDistance.objects.get_or_create(
            from_iata=o, to_iata=d,
            defaults={'distance_km': Decimal(str(km))},
        )


def ingest_sample_file(tenant, source_type: str, filename: str):
    path = SAMPLES_DIR / filename
    with open(path, 'rb') as f:
        content = f.read()
    upload = SimpleUploadedFile(filename, content, content_type='text/csv')
    rows = parse_upload(upload, 'text/csv')
    return ingest_rows(tenant, source_type, rows, filename, 'text/csv')


def mark_one_approved(tenant):
    record = NormalizedEmissionRecord.objects.filter(tenant=tenant, status=RecordStatus.PENDING).first()
    if record:
        record.status = RecordStatus.APPROVED
        record.reviewed_by = 'seed-script'
        from django.utils import timezone
        record.reviewed_at = timezone.now()
        record.save()


def main():
    print('Seeding ESG database...')
    acme, globex = seed_tenants()
    seed_airports()

    for tenant in (acme, globex):
        seed_plant_mappings(tenant)
        print(f'  Ingesting samples for {tenant.client_id}...')
        ingest_sample_file(tenant, SourceType.SAP, 'sap_fuel_procurement.csv')
        ingest_sample_file(tenant, SourceType.UTILITY, 'utility_electricity.csv')
        ingest_sample_file(tenant, SourceType.TRAVEL, 'travel_expenses.csv')
        mark_one_approved(tenant)

    print('Done.')
    print(f'  Tenants: acme, globex')
    print(f'  Records (acme): {NormalizedEmissionRecord.objects.filter(tenant=acme).count()}')


if __name__ == '__main__':
    main()
