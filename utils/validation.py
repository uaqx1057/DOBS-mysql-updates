import datetime
from decimal import Decimal, InvalidOperation


def parse_date(value):
    if not value:
        return None
    if isinstance(value, datetime.date):
        return value
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.datetime.strptime(str(value), fmt).date()
        except ValueError:
            continue
    raise ValueError("Invalid date format")


def parse_decimal(value, precision=2):
    if value is None or value == "":
        return None
    try:
        quant = Decimal(10) ** -precision
        return Decimal(str(value)).quantize(quant)
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid numeric value")


def require_keys(data, keys):
    missing = [k for k in keys if k not in data or data[k] in (None, "")]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
