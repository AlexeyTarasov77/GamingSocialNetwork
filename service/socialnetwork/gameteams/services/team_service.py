from gameteams.models import TeamJoinRequest, Team
from users.models import Profile
from django.db.models.query import QuerySet
from typing import Tuple


class TeamService:
    """Contains business logic for team management"""
    def __init__(self, team: Team) -> None:
        self.team = team

    def get_join_request(self, user_id: int) -> TeamJoinRequest:
        join_request = TeamJoinRequest.objects.get(to_team=self.team, from_user=user_id)
        return join_request

    def get_all_join_requests(self) -> QuerySet[TeamJoinRequest]:
        return TeamJoinRequest.objects.filter(to_team=self.team)

    def create_join_request(self, user_id: int) -> Tuple[TeamJoinRequest, bool]:
        join_request, created = TeamJoinRequest.objects.get_or_create(
            to_team=self.team, from_user=user_id
        )
        return (join_request, created)

    def accept_join_request(self, user_profile: Profile) -> TeamJoinRequest:
        join_request = self.get_join_request(user_profile.user_id)
        join_request.delete()
        user_profile.team = self.team
        user_profile.save()
        return join_request

    def remove_join_request(self, user_profile: Profile) -> TeamJoinRequest:
        join_request = self.get_join_request(user_profile.user_id)
        join_request.delete()
        return join_request

    def remove_member(self, user_profile: Profile) -> None:
        user_profile.team = None
        user_profile.save()
