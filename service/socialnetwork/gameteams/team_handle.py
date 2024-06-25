from .models import TeamJoinRequest, Team
from users.models import Profile
from django.db.models.query import QuerySet
from typing import Tuple
from django.contrib.auth.models import User

class TeamService:
    def __init__(self, team: Team) -> None:
        self.team = team
        
    def add_member(self, user_profile: Profile) -> None:
        user_profile.team = self.team
        user_profile.save()
        
    def check_is_member(self, user_profile: Profile) -> bool:
        return user_profile.team == self.team
        
    def create_leader_founder(self, user: User) -> None:
        self.team.leader = self.team.founder = user
        self.add_member(user.profile)
        
    def make_leader(self, user):
        self.team.leader = user
        self.team.save()
        
    def get_join_request(self, user_id: int) -> TeamJoinRequest:
        join_request = TeamJoinRequest.objects.get(
            to_team=self.team, from_user=user_id
        )
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
        self.add_member(user_profile)
        return join_request
    
    def remove_join_request(self, user_profile: Profile) -> TeamJoinRequest:
        join_request = self.get_join_request(user_profile.user_id)
        join_request.delete()
        return join_request
    
    def remove_member(self, user_profile: Profile) -> None:
        user_profile.team = None
        user_profile.save()