from typing import Any
from .redis_connection import r


class ObjectViewsMixin:
    redis_key_prefix = None

    def get_or_update_object_views(self, viewers_key, views_key):
        user_id = str(self.request.user.id)
        viewed_users_ids = r.smembers(viewers_key) or []
        if user_id not in viewed_users_ids:
            r.sadd(viewers_key, user_id)
            total_views = r.incr(views_key)
        else:
            total_views = r.get(views_key)
        return total_views

    def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base_key = f"{self.redis_key_prefix}:{self.object.id}"
        context["views_count"] = self.get_or_update_object_views(
            base_key + ":viewers",
            base_key + ":views",
        )
        return context
