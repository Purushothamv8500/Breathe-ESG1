"""CSV and JSON parsing for ingestion endpoints."""

import csv
import io
import json
from typing import Any


def parse_upload(file_obj, content_type: str = '') -> list[dict[str, Any]]:
    """
    Parse uploaded file into list of row dicts.
    Supports CSV (text/csv) and JSON array/object.
    """
    raw_bytes = file_obj.read()
    if hasattr(file_obj, 'seek'):
        file_obj.seek(0)

    name = getattr(file_obj, 'name', '') or ''
    ct = (content_type or '').lower()

    if 'json' in ct or name.endswith('.json'):
        return _parse_json(raw_bytes)

    return _parse_csv(raw_bytes)


def _parse_json(raw_bytes: bytes) -> list[dict]:
    data = json.loads(raw_bytes.decode('utf-8-sig'))
    if isinstance(data, list):
        return [row if isinstance(row, dict) else {'value': row} for row in data]
    if isinstance(data, dict):
        if 'rows' in data:
            return data['rows']
        if 'data' in data:
            return data['data']
        return [data]
    raise ValueError('JSON must be an array or object with rows/data')


def _parse_csv(raw_bytes: bytes) -> list[dict]:
    text = raw_bytes.decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]
