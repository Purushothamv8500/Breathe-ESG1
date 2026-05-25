"""
SAP fuel + procurement normalizer.

Handles inconsistent column names from OData/flat exports.
Fuel -> Scope 1 (liters). Procurement/spend -> Scope 3.
"""

from decimal import Decimal

from ingestion.dates import parse_date
from ingestion.units import normalize_fuel, to_decimal
from records.models import PlantCodeMapping, Scope, SourceType

# Column alias maps for messy SAP exports
PLANT_KEYS = ('plant', 'plant_code', 'plnt', 'werk')
DATE_KEYS = ('posting date', 'posting_date', 'budat', 'document date', 'doc_date')
QTY_KEYS = ('fuel_qty', 'quantity', 'qty', 'menge', 'consumption')
UNIT_KEYS = ('fuelunit', 'fuel_unit', 'unit', 'uom', 'meins')
MATERIAL_KEYS = ('material', 'matnr', 'material_desc', 'description')
PROCUREMENT_KEYS = ('amount', 'net_value', 'spend', 'value')


def _first(row: dict, keys: tuple) -> str | None:
    lower_map = {k.lower().strip(): v for k, v in row.items()}
    for key in keys:
        if key.lower() in lower_map and lower_map[key.lower()] not in (None, ''):
            return lower_map[key.lower()]
    return None


def _resolve_plant(tenant, code: str | None) -> tuple[str, list[str]]:
    flags = []
    if not code:
        flags.append('MISSING_FIELD')
        return '', flags
    mapping = PlantCodeMapping.objects.filter(tenant=tenant, sap_code__iexact=str(code).strip()).first()
    if mapping:
        return f'{mapping.display_name} ({mapping.region})'.strip(), flags
    flags.append('MISSING_FIELD')
    return str(code), flags


def normalize_sap_row(tenant, row: dict, row_index: int) -> dict:
    """Return dict ready for NormalizedEmissionRecord creation."""
    flags = []

    plant_code = _first(row, PLANT_KEYS)
    location, plant_flags = _resolve_plant(tenant, plant_code)
    flags.extend(plant_flags)

    date_val = _first(row, DATE_KEYS)
    activity_date = parse_date(date_val)
    if activity_date is None:
        flags.append('MISSING_FIELD')

    material = _first(row, MATERIAL_KEYS) or ''
    qty_raw = to_decimal(_first(row, QTY_KEYS))
    unit_raw = (_first(row, UNIT_KEYS) or '').strip()

    procurement_val = _first(row, PROCUREMENT_KEYS)
    is_procurement = procurement_val and (qty_raw is None or unit_raw == '')

    if is_procurement:
        scope = Scope.SCOPE_3
        category = 'procurement'
        amount = to_decimal(procurement_val)
        normalized = {
            'type': 'procurement',
            'amount': str(amount) if amount else None,
            'material': material,
            'plant_code': plant_code,
        }
        return {
            'source_type': SourceType.SAP,
            'scope': scope,
            'activity_date': activity_date,
            'category': category,
            'description': material or 'SAP procurement',
            'location': location,
            'quantity_raw': amount,
            'unit_raw': 'currency',
            'quantity_normalized': amount,
            'unit_normalized': 'currency',
            'quality_flags': list(set(flags)),
            'normalized_payload': normalized,
            'source_row_index': row_index,
        }

    # Fuel path -> Scope 1
    qty_norm, unit_norm, fuel_flags = normalize_fuel(qty_raw, unit_raw)
    flags.extend(fuel_flags)

    normalized = {
        'type': 'fuel',
        'quantity_liters': str(qty_norm) if qty_norm else None,
        'material': material,
        'plant_code': plant_code,
        'original_row': row,
    }

    return {
        'source_type': SourceType.SAP,
        'scope': Scope.SCOPE_1,
        'activity_date': activity_date,
        'category': 'fuel',
        'description': material or f'SAP fuel @ {plant_code or "unknown"}',
        'location': location,
        'quantity_raw': qty_raw,
        'unit_raw': unit_raw,
        'quantity_normalized': qty_norm,
        'unit_normalized': unit_norm,
        'quality_flags': list(set(flags)),
        'normalized_payload': normalized,
        'source_row_index': row_index,
    }
