from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import ProfileTeamsHistory, Profile

@receiver(pre_save, sender=Profile)
def update_profile_teams_history(sender, instance, **kwargs):
    try:
        last_team = Profile.objects.get(pk=instance.pk).team
    except Profile.DoesNotExist:
        last_team = None
    current_team  = instance.team
    if last_team is not None and current_team != last_team:
        if current_team is None:
            # case when user left team
            prev_team_history = ProfileTeamsHistory.objects.filter(
                profile=instance, team=last_team
            ).last()
            if prev_team_history:
                prev_team_history.date_left = timezone.now()
                prev_team_history.save()
        else:
            # case when user joined team
            ProfileTeamsHistory.objects.create(
                profile=instance, team=current_team, date_joined=timezone.now()
            )