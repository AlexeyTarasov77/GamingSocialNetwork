from posts.models import Post
from django.db.models import Count, QuerySet


class SimillarPostsByTagService:
    def __init__(self, post: Post) -> None:
        self.post = post
        
    def _get_simillar_posts(self):
        post_tags_ids = self.post.tags.values_list("id", flat=True)
        similar_posts = (
            Post.published.filter(tags__in=post_tags_ids)
            .exclude(id=self.post.id)
            .annotate(same_tags=Count("tags"))
            .select_related("author")
            .prefetch_related("tags", "liked", "saved", "comments")
            .order_by("-same_tags", "-time_publish")[:4]
        )
        return similar_posts
    
    def execute(self) -> QuerySet[Post]:
        return self._get_simillar_posts()