from datetime import datetime, timezone


def get_current_dt() -> datetime:
    return datetime.now(tz=timezone.utc).replace(microsecond=0)
