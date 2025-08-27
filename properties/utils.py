from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    # Try to fetch from Redis
    properties = cache.get("all_properties")

    if properties is None:
        # Cache miss → fetch from DB
        properties = list(Property.objects.all().values("id", "title", "description", "price"))
        # Store in Redis for 1 hour (3600 seconds)
        cache.set("all_properties", properties, 3600)

    return properties


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
    total = hits + misses

    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    # Log metrics for debugging
    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics