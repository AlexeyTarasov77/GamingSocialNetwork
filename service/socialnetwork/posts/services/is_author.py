from django.contrib.auth.models import User
from django.db.models import Model


class CheckIsAuthorService:
    def __init__(self, obj: Model, user: User, obj_owner_field_name: str) -> None:
        self.user = user
        self.object_author = getattr(obj, obj_owner_field_name)
        
    def _is_author(self):
        return self.object_author == self.user
    
    def execute(self) -> bool:
        return self._is_author()