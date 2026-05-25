"""
Corporate travel normalizer (Concur/Navan style) -> Scope 3, km.

Uses AirportDistance lookup; default 800 km if pair unknown.
"""

from decimal import Decimal

from ingestion.dates import parse_date
from ingestion.units import normalize_distance_km, to_decimal
from records.models import AirportDistance, Scope, SourceType

TYPE_KEYS = ('type', 'category', 'expense_type', 'transaction_type')
FROM_KEYS = ('from', 'origin', 'departure', 'from_airport')
TO_KEYS = ('to', 'destination', 'arrival', 'to_airport')
DATE_KEYS = ('start_date', 'transaction_date', 'date', 'departure_date')
DISTANCE_KEYS = ('distance', 'distance_km', 'miles')
EMPLOYEE_KEYS = ('employee', 'traveler', 'name')


def _first(row: dict, keys: tuple) -> str | None:
    lower_map = {k.lower().strip(): v for k, v in row.items()}
    for key in keys:
        if key.lower() in lower_map and lower_map[key.lower()] not in (None, ''):
            return lower_map[key.lower()]
    return None


def _lookup_airport_km(origin: str, dest: str) -> tuple[Decimal, bool]:
    """Return (km, from_lookup)."""
    o = (origin or '').strip().upper()[:3]
    d = (dest or '').strip().upper()[:3]
    if len(o) < 3 or len(d) < 3:
        return Decimal('0'), False
    pair = AirportDistance.objects.filter(from_iata=o, to_iata=d).first()
    if pair:
        return pair.distance_km, True
    pair_rev = AirportDistance.objects.filter(from_iata=d, to_iata=o).first()
    if pair_rev:
        return pair_rev.distance_km, True
    return Decimal('800'), False  # reasonable default for unknown pair


def _ground_hotel_km(travel_type: str) -> Decimal:
    t = (travel_type or '').lower()
    if 'hotel' in t:
        return Decimal('50')
    if 'ground' in t or 'taxi' in t or 'rail' in t or 'train' in t:
        return Decimal('30')
    if 'car' in t or 'rental' in t:
        return Decimal('100')
    return Decimal('25')


def normalize_travel_row(tenant, row: dict, row_index: int) -> dict:
    flags = []

    travel_type = _first(row, TYPE_KEYS) or 'unknown'
    origin = _first(row, FROM_KEYS)
    dest = _first(row, TO_KEYS)
    activity_date = parse_date(_first(row, DATE_KEYS))
    if activity_date is None:
        flags.append('MISSING_FIELD')

    employee = _first(row, EMPLOYEE_KEYS) or ''
    explicit_dist = to_decimal(_first(row, DISTANCE_KEYS))

    t_lower = travel_type.lower()
    if 'flight' in t_lower or 'air' in t_lower:
        category = 'flight'
        if not origin or not dest:
            flags.append('MISSING_FIELD')
        if explicit_dist is not None:
            km = explicit_dist
            from_lookup = False
        else:
            km, from_lookup = _lookup_airport_km(origin, dest)
            if not from_lookup:
                flags.append('MISSING_FIELD')
    else:
        category = travel_type
        km = _ground_hotel_km(travel_type)
        if explicit_dist is not None:
            km = explicit_dist

    qty_norm, unit_norm, dist_flags = normalize_distance_km(km, 'km')
    flags.extend(dist_flags)

    normalized = {
        'type': category,
        'origin': origin,
        'destination': dest,
        'employee': employee,
        'distance_km': str(qty_norm) if qty_norm else None,
        'original_row': row,
    }

    return {
        'source_type': SourceType.TRAVEL,
        'scope': Scope.SCOPE_3,
        'activity_date': activity_date,
        'category': category,
        'description': f'{travel_type}: {origin or "?"} -> {dest or "?"} ({employee})'.strip(),
        'location': f'{origin}-{dest}' if origin and dest else '',
        'quantity_raw': km,
        'unit_raw': 'km',
        'quantity_normalized': qty_norm,
        'unit_normalized': unit_norm,
        'quality_flags': list(set(flags)),
        'normalized_payload': normalized,
        'source_row_index': row_index,
    }
