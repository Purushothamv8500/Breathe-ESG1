"""
Utility electricity CSV normalizer -> Scope 2, kWh.
"""

from ingestion.dates import parse_date
from ingestion.units import normalize_energy, to_decimal
from records.models import Scope, SourceType

METER_KEYS = ('meter_id', 'meter', 'account', 'service_point')
START_KEYS = ('billing_start', 'period_start', 'start_date', 'from_date')
END_KEYS = ('billing_end', 'period_end', 'end_date', 'to_date')
USAGE_KEYS = ('usage', 'consumption', 'kwh', 'energy')
UNIT_KEYS = ('usage_uom', 'uom', 'unit', 'usage_unit')
TARIFF_KEYS = ('tariff', 'rate_schedule', 'plan')


def _first(row: dict, keys: tuple) -> str | None:
    lower_map = {k.lower().strip(): v for k, v in row.items()}
    for key in keys:
        if key.lower() in lower_map and lower_map[key.lower()] not in (None, ''):
            return lower_map[key.lower()]
    return None


def _billing_mid_date(start, end):
    s, e = parse_date(start), parse_date(end)
    if s and e:
        from datetime import timedelta
        delta = (e - s) / 2
        return s + delta
    return s or e


def normalize_utility_row(tenant, row: dict, row_index: int) -> dict:
    flags = []

    meter = _first(row, METER_KEYS)
    if not meter:
        flags.append('MISSING_FIELD')

    activity_date = _billing_mid_date(_first(row, START_KEYS), _first(row, END_KEYS))
    if activity_date is None:
        flags.append('MISSING_FIELD')

    qty_raw = to_decimal(_first(row, USAGE_KEYS))
    unit_raw = (_first(row, UNIT_KEYS) or 'kWh').strip()
    tariff = _first(row, TARIFF_KEYS) or ''

    qty_norm, unit_norm, energy_flags = normalize_energy(qty_raw, unit_raw)
    flags.extend(energy_flags)

    normalized = {
        'type': 'electricity',
        'meter_id': meter,
        'tariff': tariff,
        'billing_start': _first(row, START_KEYS),
        'billing_end': _first(row, END_KEYS),
        'kwh': str(qty_norm) if qty_norm else None,
        'original_row': row,
    }

    return {
        'source_type': SourceType.UTILITY,
        'scope': Scope.SCOPE_2,
        'activity_date': activity_date,
        'category': 'electricity',
        'description': f'Meter {meter or "unknown"}' + (f' ({tariff})' if tariff else ''),
        'location': meter or '',
        'quantity_raw': qty_raw,
        'unit_raw': unit_raw,
        'quantity_normalized': qty_norm,
        'unit_normalized': unit_norm,
        'quality_flags': list(set(flags)),
        'normalized_payload': normalized,
        'source_row_index': row_index,
    }
