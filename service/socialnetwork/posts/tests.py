from django.test import TestCase, RequestFactory, Client
from .views import ListPosts, DetailPost
from .models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model
from . import forms
import json
# Create your tests here.
User = get_user_model()
class ListPostsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.obj = Post.objects.create(name='Test', content='Test', author_id=self.user.id)

    def test_get_request(self):
        response = self.client.get(reverse('posts:list-posts'))
        cob = ListPosts.context_object_name
        self.assertTrue(len(response.context[cob]) > 0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[cob][0].id, self.obj.id)
        self.assertTemplateUsed(response, 'posts/list.html')
        
class DetailPostTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.obj = Post.objects.create(name='DetailTest', content='Detail Test Content', author_id=self.user.id)
        
    def test_get_request(self):
        print(self.obj.id)
        # request = self.factory.get(reverse('posts:detail-post', kwargs={'post_id': self.obj.id}))
        # response = DetailPost.as_view()(request)
        response = self.client.get(reverse('posts:detail-post', kwargs={'post_id': self.obj.id}))
        cob = DetailPost.context_object_name
        self.assertIsNotNone(response.context[cob])
        self.assertEqual(response.context[cob].id, self.obj.id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/detail.html')
        self.assertFalse(response.context['is_owner'])
        
        
class AddPostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username=self.user.username, password='12345')
    def test_post_request(self):
        data = {
            'name': 'Testing Add Post',
            'content': 'Test Content',
            'author_id': self.user.id
        }
        response = self.client.post(reverse('posts:add-post'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(name=data.name, content=data.content).exists())
    def test_get_request(self):
        response = self.client.get(reverse('posts:add-post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create.html')
        self.assertEqual(response.content['form'], forms.CreatePostForm())
        