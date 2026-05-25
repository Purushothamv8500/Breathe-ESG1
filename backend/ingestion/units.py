"""Unit normalization helpers."""

from decimal import Decimal, InvalidOperation

TO_KWH = {
    'kwh': Decimal('1'),
    'kw-h': Decimal('1'),
    'mwh': Decimal('1000'),
    'megawatt-hour': Decimal('1000'),
}

TO_LITERS = {
    'l': Decimal('1'),
    'liter': Decimal('1'),
    'liters': Decimal('1'),
    'litre': Decimal('1'),
    'litres': Decimal('1'),
    'gal': Decimal('3.78541'),
    'gallon': Decimal('3.78541'),
    'gallons': Decimal('3.78541'),
    'kg': Decimal('1'),  # mass fuel treated 1:1 for demo when no density
}

OUTLIER_KWH = Decimal('1000000')
OUTLIER_LITERS = Decimal('50000')
OUTLIER_KM = Decimal('20000')


def to_decimal(value) -> Decimal | None:
    if value is None or value == '':
        return None
    try:
        cleaned = str(value).replace(',', '').strip()
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return None


def normalize_energy(quantity, unit: str) -> tuple[Decimal | None, str | None, list[str]]:
    flags = []
    if quantity is None:
        return None, None, ['MISSING_FIELD']
    u = (unit or '').lower().strip()
    factor = TO_KWH.get(u)
    if factor is None:
        return None, None, ['INVALID_UNIT']
    result = quantity * factor
    if result > OUTLIER_KWH:
        flags.append('SUSPICIOUS_VALUE')
    return result, 'kWh', flags


def normalize_fuel(quantity, unit: str) -> tuple[Decimal | None, str | None, list[str]]:
    flags = []
    if quantity is None:
        return None, None, ['MISSING_FIELD']
    u = (unit or '').lower().strip()
    factor = TO_LITERS.get(u)
    if factor is None:
        return None, None, ['INVALID_UNIT']
    result = quantity * factor
    if result > OUTLIER_LITERS:
        flags.append('SUSPICIOUS_VALUE')
    return result, 'L', flags


def normalize_distance_km(quantity, unit: str = 'km') -> tuple[Decimal | None, str | None, list[str]]:
    flags = []
    if quantity is None:
        return None, None, ['MISSING_FIELD']
    u = (unit or 'km').lower().strip()
    if u in ('km', 'kilometer', 'kilometers'):
        result = quantity
    elif u in ('mi', 'mile', 'miles'):
        result = quantity * Decimal('1.60934')
    else:
        return None, None, ['INVALID_UNIT']
    if result > OUTLIER_KM:
        flags.append('SUSPICIOUS_VALUE')
    return result, 'km', flags
