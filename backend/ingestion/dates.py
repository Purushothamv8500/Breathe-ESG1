"""Flexible enterprise date parsing."""

from datetime import date, datetime

from dateutil import parser as date_parser


def parse_date(value) -> date | None:
    if not value or str(value).strip() == '':
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    try:
        dt = date_parser.parse(str(value).strip(), dayfirst=False)
        return dt.date()
    except (ValueError, TypeError, OverflowError):
        try:
            dt = date_parser.parse(str(value).strip(), dayfirst=True)
            return dt.date()
        except (ValueError, TypeError, OverflowError):
            return None
