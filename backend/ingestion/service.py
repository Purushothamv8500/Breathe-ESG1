"""Orchestrates raw storage + normalization for all sources."""

from records.models import NormalizedEmissionRecord, RawDataRecord, SourceType

from .normalizers import normalize_sap_row, normalize_travel_row, normalize_utility_row

NORMALIZERS = {
    SourceType.SAP: normalize_sap_row,
    SourceType.UTILITY: normalize_utility_row,
    SourceType.TRAVEL: normalize_travel_row,
}


def ingest_rows(tenant, source_type: str, rows: list, filename: str = '', content_type: str = '') -> dict:
    """
    Store immutable raw payload and create normalized emission records.
    Returns summary dict for API response.
    """
    raw = RawDataRecord.objects.create(
        tenant=tenant,
        source_type=source_type,
        payload={'rows': rows, 'row_count': len(rows)},
        filename=filename,
        content_type=content_type,
    )

    normalizer = NORMALIZERS[source_type]
    record_ids = []
    warnings = []

    for idx, row in enumerate(rows):
        data = normalizer(tenant, row, idx)
        if data.get('quality_flags'):
            warnings.append({'row': idx, 'flags': data['quality_flags']})

        record = NormalizedEmissionRecord.objects.create(
            tenant=tenant,
            raw_record=raw,
            source_type=data['source_type'],
            scope=data['scope'],
            activity_date=data.get('activity_date'),
            category=data.get('category', ''),
            description=data.get('description', ''),
            location=data.get('location', ''),
            quantity_raw=data.get('quantity_raw'),
            unit_raw=data.get('unit_raw') or '',
            quantity_normalized=data.get('quantity_normalized'),
            unit_normalized=data.get('unit_normalized') or '',
            quality_flags=data.get('quality_flags', []),
            normalized_payload=data.get('normalized_payload', {}),
            source_row_index=data.get('source_row_index', idx),
        )
        record_ids.append(record.id)

    return {
        'raw_id': raw.id,
        'record_ids': record_ids,
        'row_count': len(rows),
        'warnings': warnings,
    }
