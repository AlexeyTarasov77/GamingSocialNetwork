from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import ProfileTeamsHistory, Profile


# @receiver(pre_save, sender=Profile)
# def update_profile_teams_history(sender, instance, **kwargs):
#     last_team = Profile.objects.get(pk=instance.pk).team
#     if instance.team != last_team and last_team is not None:
#         prev_team_history = ProfileTeamsHistory.objects.filter(
#             profile=instance, team=last_team
#         ).last()
#         if prev_team_history:
#             prev_team_history.date_left = timezone.now()
#             prev_team_history.save()
#         else:
#             ProfileTeamsHistory.objects.create(
#                 profile=instance, team=instance.team, date_joined=timezone.now()
#             )
#         return


@receiver(pre_save, sender=Profile)
def update_profile_teams_history(sender, instance, **kwargs):
    last_team = Profile.objects.get(pk=instance.pk).team
    if instance.team != last_team and last_team is not None:
        print(instance.team, last_team)
        if instance.team is None:
            prev_team_history = ProfileTeamsHistory.objects.filter(
                profile=instance, team=last_team
            ).last()
            prev_team_history.date_left = timezone.now()
            prev_team_history.save()
        else:
            ProfileTeamsHistory.objects.create(
                profile=instance, team=instance.team, date_joined=timezone.now()
            )
    print("nothing happen")