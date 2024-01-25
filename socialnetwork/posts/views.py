from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Post
from django.db.models import Count
from . import forms
from django.core.mail import send_mail
from decouple import config
from rest_framework import views, permissions
from .serializers import LikeSerializer
from rest_framework.response import Response

# Create your views here.
class ListPosts(generic.ListView):
    template_name = 'posts/list.html'
    queryset = Post.published.annotate(count_likes=Count('liked')).order_by('-count_likes')
    context_object_name = 'posts_list'
    paginate_by = 2
    
class DetailPost(generic.DetailView):
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        post = self.get_object()
        context = super().get_context_data(**kwargs)
        context["is_owner"] = False
        if self.request.user == post.author:
            context["is_owner"] = True
        context["parent_comments"] = post.comment.filter(reply=None)
        return context
    
    
class DeletePost(generic.DeleteView):
    template_name = 'delete.html'
    model = Post
    success_url = reverse_lazy('posts:list')
    
class UpdatePost(generic.UpdateView):
    template_name = 'update.html'
    model = Post
    fields = ['name', 'content', 'status', 'photo']
    
# class LikePost(generic.CreateView):
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             p_id = request.POST.get('post_id')
#             post = get_object_or_404(Post, id=p_id)
            
#             if request.user in post.liked.all():
#                 post.liked.remove(request.user)
#                 return JsonResponse({'likes_count': post.liked.count(), 'is_liked': False})
#             else:
#                 post.liked.add(request.user)
#                 return JsonResponse({'likes_count': post.liked.count(), 'is_liked': True})
            
#         else: return HttpResponse("<h1>Авторизуйтесь для того что бы лайкнуть пост</h1>")

# Share post by email address
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False # tmp variable to check if email sent successfully
    if request.method == 'POST':
        form = forms.ShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['username'] = post.author # move data to hidden form field
            cd['email'] = post.author.email # # move data to hidden form field
            post_url = request.build_absolute_uri(post.get_absolute_url()) 
            subject = f"{cd['username']} recommends you read: {post.name}"
            message = f"Read {post.name} at {post_url}\n\n" \
                f"{cd['username']}\'s comments: {cd['notes']}"
            send_mail(subject, message, config('EMAIL_HOST_USER'), [cd['to']])
            sent = True 
    else:
        form = forms.ShareForm()
    return render(request, 'posts/share_post.html', {'post': post,
    'form': form, 'sent': sent})
    
    
    
# API'S 
    
class LikePostAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] # Return data only for authenticated users
    def post(self, request, *args, **kwargs):
            p_id = request.POST.get('post_id') # get id of current post from req
            post = get_object_or_404(Post, id=p_id)
            
            if request.user in post.liked.all(): # if current user already liked current post
                post.liked.remove(request.user) # remove him out of the list (unlike)
                data = {'likes_count': post.liked.count(), 'is_liked': False} # data to return 
            else: # if user hadn't liked this post yet add him to the list
                post.liked.add(request.user) 
                data = {'likes_count': post.liked.count(), 'is_liked': True} # data to return 
            serializer = LikeSerializer(data)
            return Response(serializer.data) # return serialized cleaned data
    
        
        

        