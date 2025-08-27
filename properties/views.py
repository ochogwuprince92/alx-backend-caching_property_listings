from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from .models import Property
from .utils import get_redis_cache_metrics

@cache_page(60 * 15)  # cache for 15 minutes
@require_GET
def property_list(request):
    properties = Property.objects.all().values("id", "title", "description", "price")
    return JsonResponse({
        "data": list(properties)
    })

def cache_metrics_view(request):
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)