from django.core.cache import cache


def get_from_cache_or_compute(cache_key, callback):
    data = cache.get(cache_key)
    if data:
        return data
    return callback()
