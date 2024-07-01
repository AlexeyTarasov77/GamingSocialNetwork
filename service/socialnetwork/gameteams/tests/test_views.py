from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import activate
from users.tests.factories import UserFactory

from .factories import TeamFactory


# Create your tests here.
class TeamDetailTestCase(TestCase):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.user1, self.user2 = UserFactory.create_batch(2)
        self.client.login(username=self.user1.username, password="password123")
        self.team = TeamFactory.create(leader=self.user2, founder=self.user2)
        self.url = reverse("teams:team_leave", kwargs={"slug": self.team.slug})

    def test_team_leave_not_allowed(self):
        """In case that user arent in team"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_team_leave_allowed(self):
        """Positive test case"""
        self.user1.profile.team = self.team
        self.user1.profile.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TeamHandleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1, self.user2, self.user3 = UserFactory.create_batch(3)
        self.team = TeamFactory.create(leader=self.user1, founder=self.user1)
        self.user1.profile.team = self.team
        self.user1.profile.save()
        self.url = reverse(
            "teams:remove_team_member", kwargs={"pk": self.user3.profile.pk}
        )

    def test_kick_member_not_allowed(self):
        """In case the user is not the team leader"""
        self.client.login(username=self.user2.username, password="password123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_kick_member_not_found(self):
        """In case the user is not found in team"""
        self.client.login(username=self.user1.username, password="password123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_kick_member_found(self):
        """Positive test case"""
        self.client.login(username=self.user1.username, password="password123")
        self.user3.profile.team = self.team
        self.user3.profile.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)


class TeamListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1, self.user2 = UserFactory.create_batch(2)
        self.client.login(username=self.user1.username, password="password123")
        self.team1 = TeamFactory(leader=self.user1, founder=self.user1)
        self.team2 = TeamFactory(leader=self.user2, founder=self.user2)

    def test_team_list(self):
        """Positive test case"""
        response = self.client.get(reverse("teams:team_list"))
        self.assertEqual(response.status_code, 200)


class TeamJoinTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = UserFactory.create()
        self.team = TeamFactory.create(leader=self.user1, founder=self.user1)

    def test_team_join(self):
        """Positive test case"""
        self.client.login(username=self.user1.username, password="password123")
        response = self.client.post(
            reverse("teams:team_join", kwargs={"slug": self.team.slug})
        )
        self.assertEqual(response.status_code, 200)
