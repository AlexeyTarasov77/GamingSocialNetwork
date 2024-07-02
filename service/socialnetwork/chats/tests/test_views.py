from django.test import TestCase, Client
from django.urls import reverse
from .factories import ChatRoomFactory
from chats.models import ChatRoom
from users.tests.factories import UserFactory
from chats.services.chats_service import ChatsService
from django.utils.translation import activate
from django.conf import settings
import faker


fuzzy = faker.Faker()
# python3 manage.py test chats


class LoginTestMixin:
    def _test_redirect_to_login(self, response):
        self.assertTrue(response.status_code, 302)
        redirect_url = reverse(settings.LOGIN_URL) + "?next=" + self.url
        self.assertRedirects(response, redirect_url)


class GroupChatRoomCreateTest(TestCase, LoginTestMixin):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.users = UserFactory.create_batch(3)
        self.user_admin, *_ = self.users
        self.data = {
            "name": fuzzy.text(10),
            "members": [user.id for user in self.users],
        }
        self.url = reverse("chats:create-group")

    def test_no_auth(self):
        response = self.client.post(self.url, self.data)
        self._test_redirect_to_login(response)
        self.assertFalse(
            ChatRoom.objects.filter(
                name=self.data["name"],
                members__in=self.data["members"],
                type=ChatRoom.TYPE_CHOICES[0][0],
            ).exists()
        )

    def test_auth(self):
        self.client.force_login(self.user_admin)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ChatRoom.objects.filter(
                name=self.data["name"],
                members__in=self.data["members"],
                type=ChatRoom.TYPE_CHOICES[0][0],
            ).exists()
        )


class PersonalChatRoomCreateTest(TestCase, LoginTestMixin):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.users = UserFactory.create_batch(2)
        self.user_admin, *_ = self.users
        self.data = {"members": [user.id for user in self.users]}
        self.url = reverse("chats:create-personal")

    def _check_chatroom_exists(self):
        members_users = [
            user for user in self.users if user.id in self.data["members"]
        ][::-1]
        return ChatRoom.objects.filter(
            name=ChatsService.generate_chat_name_by_members(members_users),
            members__in=self.data["members"],
            type=ChatRoom.TYPE_CHOICES[1][0],
        ).exists()

    def test_no_auth(self):
        response = self.client.post(self.url, self.data)
        self._test_redirect_to_login(response)
        self.assertFalse(self._check_chatroom_exists())

    def test_auth(self):
        self.client.force_login(self.user_admin)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self._check_chatroom_exists())

    def test_too_many_members(self):
        self.client.force_login(self.user_admin)
        self.data["members"].append(UserFactory.create().id)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self._check_chatroom_exists())


class ListChatsTest(TestCase, LoginTestMixin):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.user = UserFactory.create()
        members = UserFactory.create_batch(3)
        self.chat = ChatRoomFactory.create(
            admin=self.user, members=[member.pk for member in members]
        )
        self.url = reverse("chats:list")

    def test_auth(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/list_chats.html")

    def test_with_ajax(self):
        self.client.force_login(self.user)
        response = self.client.get(
            self.url, headers={"X-Requested-With": "XMLHttpRequest"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/includes/list_chats_sidebar.html")

    def test_no_auth(self):
        response = self.client.get(self.url)
        self._test_redirect_to_login(response)


class ChatRoomDetailTest(TestCase, LoginTestMixin):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.chat_admin = UserFactory.create()
        members = UserFactory.create_batch(3)
        self.chat = ChatRoomFactory.create(
            admin=self.chat_admin, members=[member.pk for member in members] + [self.chat_admin.pk],
        )
        self.url = reverse("chats:detail", args=[self.chat.id])

    def test_auth(self):
        self.client.force_login(self.chat_admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/chatroom.html")

    def test_no_auth(self):
        response = self.client.get(self.url)
        self._test_redirect_to_login(response)

    def test_with_ajax(self):
        self.client.force_login(self.chat_admin)
        response = self.client.get(
            self.url, headers={"X-Requested-With": "XMLHttpRequest"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/partials/chatroom_p.html")


class ChatRoomMemberRemoveTest(TestCase, LoginTestMixin):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.chat_admin = UserFactory.create()
        members = UserFactory.create_batch(3)
        self.chat = ChatRoomFactory.create(
            admin=self.chat_admin,
            members=[member.pk for member in members] + [self.chat_admin.pk],
        )
        self.url = reverse("chats:remove-member", args=[self.chat.id])
        
    def _get_chat_member(self):
        return self.chat.members.exclude(id=self.chat_admin.id).first()

    # def test_no_auth(self):
    #     response = self.client.post(self.url)
    #     self._test_redirect_to_login(response)

    def test_leave_admin(self):
        self.client.force_login(self.chat_admin)
        response = self.client.post(self.url, {"target_user_id": self.chat_admin.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self._check_chatroom_deleted())

    def _check_chatroom_deleted(self) -> bool:
        return not ChatRoom.objects.filter(pk=self.chat.id).exists()

    def test_leave_member(self):
        member = self._get_chat_member()
        self.client.force_login(member)
        response = self.client.post(self.url, {"target_user_id": member.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self._check_chatroom_deleted())

    def test_leave_non_member(self):
        self.client.force_login(self.chat_admin)
        response = self.client.post(
            self.url, {"target_user_id": UserFactory.create().id}
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self._check_chatroom_deleted())

    def test_remove_forbidden(self):
        member = self._get_chat_member()
        self.client.force_login(member)
        response = self.client.post(self.url, {"target_user_id": self.chat_admin.id})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self._check_chatroom_deleted())
        
    def test_remove_allowed(self):
        self.client.force_login(self.chat_admin)
        response = self.client.post(self.url, {"target_user_id": self._get_chat_member().id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self._check_chatroom_deleted())
        
    def test_remove_no_members_left(self):
        member = self._get_chat_member()
        self.chat = ChatRoomFactory.create(admin=self.chat_admin, members=[member.id])
        url = reverse("chats:remove-member", args=[self.chat.id])
        self.client.force_login(self.chat_admin)
        response = self.client.post(url, {"target_user_id": member.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self._check_chatroom_deleted())

