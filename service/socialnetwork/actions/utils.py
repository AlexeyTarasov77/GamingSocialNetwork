from datetime import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action
from django.contrib.auth.models import User

def create_action(user: User, verb: str, target: ContentType = None) -> bool | Action:
    now = timezone.now()
    last_min = now - timezone.timedelta(minutes=1)
    simillar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_min)
    if target:
        simillar_actions = simillar_actions.filter(target_id=target.id)
        
    if not simillar_actions:
        action = Action(
            user = user,
            verb = verb,
            target = target
        )
        action.save()
        return action
    return False