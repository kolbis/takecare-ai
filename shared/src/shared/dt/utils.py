from datetime import datetime, timezone, timedelta


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def from_unix(timestamp: int | float) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def to_unix(dt: datetime) -> int:
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware.")
    return int(dt.timestamp())


def utc_cutoff(hours: int) -> datetime:
    return utc_now() - timedelta(hours=hours)
