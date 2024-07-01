from typing import Final

from django.contrib.auth import get_user_model

CACHE_KEYS = {
    "POSTS_LIST_VERSION": "posts_feed_version",
    "POSTS_LIST": "posts_feed_for_user_{user_id}_params_{post_type}_{tag_slug}_v{version}",
    "POSTS_DETAIL": "posts_detail_{post_id}_{version}",
    "POSTS_DETAIL_VERSION": "posts_detail_version",
}

count_users = get_user_model().objects.count()
# required amount of likes or comments for post to be in recommendations
TOTAL_LIKES_REQUIRED: Final[int] = count_users // 3
TOTAL_COMMENTS_REQUIRED: Final[int] = count_users // 4
