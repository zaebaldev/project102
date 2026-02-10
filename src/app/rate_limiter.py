from slowapi import Limiter
from slowapi.util import get_remote_address

from core.config import settings


def get_default_rate_limit() -> str:
    """Get default rate limit string from settings.

    Returns a rate limit string like "100/minute" or "60/second".
    """
    requests = settings.rate_limiter.default_requests
    period = settings.rate_limiter.default_period

    # Convert period to a human-readable format
    period_map = {
        60: "minute",
        3600: "hour",
        86400: "day",
    }

    if period in period_map:
        return f"{requests}/{period_map[period]}"
    # For custom periods, use "per X seconds"
    return f"{requests}/{period} seconds"


limiter = Limiter(
    key_func=get_remote_address,
    # default_limits=[get_default_rate_limit()], # If you want to set a default rate limit to all routers
    storage_uri=str(settings.redis.url),
)
