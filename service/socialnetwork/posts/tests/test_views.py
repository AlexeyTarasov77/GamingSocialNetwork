from django.test import TestCase, Client
from posts.views import ListPosts, DetailPost
from .factories import PostFactory
from users.tests.factories import UserFactory
from posts.models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from posts import forms

# Create your tests here.
User = get_user_model()


class ListPostsTestCase(TestCase):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.obj = PostFactory.create()

    def test_get_request(self):
        response = self.client.get(reverse("posts:list-posts"))
        posts = ListPosts.context_object_name
        self.assertTrue(len(response.context[posts]) == 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/list.html")


class DetailPostTestCase(TestCase):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.obj = PostFactory.create()

    def test_get_request(self):
        print(self.obj.id)
        response = self.client.get(
            reverse("posts:detail-post", kwargs={"post_id": self.obj.id})
        )
        post = DetailPost.context_object_name
        self.assertIsNotNone(response.context[post])
        self.assertEqual(response.context[post].id, self.obj.id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/detail.html")
        self.assertFalse(response.context["is_owner"])


class AddPostTestCase(TestCase):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)

    def test_create(self):
        data = {
            "title": "Testing Add Post",
            "content": "Test Content",
            "author_id": self.user.id,
        }
        response = self.client.post(
            reverse("posts:add-post"),
            data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Post.objects.filter(**data).exists()
        )

    def test_view(self):
        response = self.client.get(reverse("posts:add-post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/create.html")
        self.assertIsInstance(response.context["form"], forms.CreatePostForm)
