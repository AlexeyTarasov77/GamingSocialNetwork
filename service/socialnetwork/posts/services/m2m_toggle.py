from django.contrib.auth.models import User
from django.db.models import Model


class ToggleM2MAbstractService:
    print("ToggleM2MAbstractService")
    def __init__(self, obj: Model, m2m_field_name: str, user: User) -> None:
        self.obj = obj
        self.m2m_field = getattr(obj, m2m_field_name)
        self.user = user
    def _toggle_m2m_relationship(self) -> bool:
        print("ToggleM2MAbstractService._toggle_m2m_relationship")
        """    
        Toggle a Many-to-Many relationship for a given object, field, and user.
        (for liking, saving, and simillar actions with objects)

        Args:
            obj: The object to modify the M2M relationship on.
            m2m_field_name: The name of the M2M field as a string.
            user: The user to add/remove from the M2M field.

        Returns:
            bool: False if the user is already in the M2M field, True otherwise.
        """
        print(self.m2m_field.all(), self.user)
        if self.m2m_field.filter(id=self.user.id).exists():
            self.m2m_field.remove(self.user)
            return False
        else:
            self.m2m_field.add(self.user)
            return True
        
    def execute(self) -> bool:
        print("ToggleM2MAbstractService.execute")
        return self._toggle_m2m_relationship()

class ToggleLikeService(ToggleM2MAbstractService):
    print("ToggleLikeService")
    def __init__(self, obj: Model, user: User) -> None:
        super().__init__(obj, "liked", user)
        
class ToggleSaveService(ToggleM2MAbstractService):
    def __init__(self, obj: Model, user: User) -> None:
        super().__init__(obj, "saved", user)
        


    
    

    
    