from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """Return all properties, cached in Redis for 1 hour."""
    all_properties = cache.get("all_properties")
    if all_properties is None:
        from .models import Property
        all_properties = list(Property.objects.all().values())
        cache.set("all_properties", all_properties, 3600)
    return all_properties


def get_redis_cache_metrics():
    """Retrieve Redis cache hit/miss metrics and calculate hit ratio."""
    # Get the Redis client from django-redis
    redis_client = cache.client.get_client()

    # Fetch Redis info
    info = redis_client.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total_requests = hits + misses

    hit_ratio = hits / total_requests if total_requests > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    # Log metrics (as required, using error level)
    logger.error(f"Redis Cache Metrics: {metrics}")

    return metrics