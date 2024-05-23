from django.core.cache import cache

def check_cache(cache_key, callback):
    data = cache.get(cache_key)
    if data:
        return data
    else:
        return callback()