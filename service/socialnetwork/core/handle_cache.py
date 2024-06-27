from django.core.cache import cache
from functools import wraps
from typing import Callable, Any


class HandleCacheService:
    """
    Class that handles caching operations.
    """

    @staticmethod
    def get_from_cache_or_compute(
        cache_key: str, callback: Callable, cache_timeout: int | None = None
    ) -> Any:
        """
        Retrieves data from cache if it exists, otherwise computes and stores it.

        Parameters:
            cache_key (str): The key used to store the cached result in the cache.
            callback (Callable[[], Any]): The function that computes and returns the result.

        Returns:
            Any: The cached or computed result.
        """
        data = cache.get(cache_key)
        if data:
            return data
        computed_data = callback()
        cache.set(cache_key, computed_data, cache_timeout)
        return computed_data

    @staticmethod
    def invalidate_cache_version(cache_version_key: str) -> int:
        """
        Increments the cache version by 1 and returns the new version.

        Parameters:
            cache_version_key (str): The key used to store the cache version in the cache.

        Returns:
            int: The new cache version.
        """
        new_version = cache.get(cache_version_key, 0) + 1
        print("CACHE INVALIDATION")
        print(cache_version_key, new_version)
        cache.set(cache_version_key, new_version)
        return new_version


def use_cache(cache_timeout: int | None = None) -> Callable:
    """
    Decorator function that caches the result of a function call using the provided cache key.

    Returns:
        decorator (function): The decorator function that wraps the original function
        and caches its result.

    Example:
        @use_cache("my_function_result")
        def my_function(arg1, arg2):
            # Function logic here
            return result

        # Call the function with arguments
        result = my_function(arg1, arg2)

        The result will be retrieved from the cache if it exists,
        otherwise it will be computed and stored in the cache.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = self.cache_key
            return HandleCacheService.get_from_cache_or_compute(
                cache_key, lambda: func(self, *args, **kwargs), cache_timeout
            )

        return wrapper

    return decorator
