from .models import TeamJoinRequest

class TeamHandle:
    def __init__(self, team):
        self.team = team
        
    def get_join_request(self, user):
        join_request = TeamJoinRequest.objects.get(
            to_team=self.team, from_user=user
        )
        return join_request
    
    def get_all_join_requests(self):
        return TeamJoinRequest.objects.filter(to_team=self.team)

    def create_join_request(self, user):
        join_request = TeamJoinRequest.objects.get_or_create(
            to_team=self.team, from_user=user
        )
        return join_request
    
    def accept_join_request(self, user):
        join_request = self.get_join_request(user)
        join_request.delete()
        self.team.members.add(user)
        return self.team.members
    
    def remove_join_request(self, user):
        join_request = self.get_join_request(user)
        join_request.delete()
        return self.team
    
    def remove_member(self, user):
        self.team.members.remove(user)
        return self.team