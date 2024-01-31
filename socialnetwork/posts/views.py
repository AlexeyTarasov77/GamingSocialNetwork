from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.template.exceptions import TemplateDoesNotExist
from .models import Post, Comment
from django.db.models import Count
from . import forms
from django.core.mail import send_mail
from decouple import config
from rest_framework import views, permissions
from .serializers import LikeSerializer
from rest_framework.response import Response
from taggit.models import Tag

# Create your views here.
class ListPosts(generic.ListView):
    template_name = 'posts/list.html'
    context_object_name = 'posts_list'
    paginate_by = 2
    def get_queryset(self):
        queryset = Post.published.annotate(count_likes=Count('liked'), count_comments=Count('comment_post')).order_by('-count_likes', '-count_comments')
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug is not None:
            tag = get_object_or_404(Tag, slug=tag_slug) 
            queryset = queryset.filter(tags__in=[tag])
        return queryset
    
    
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
        context["form"] = forms.CommentForm
        context["filtered_comments"] = post.comment_post.filter(is_active=True)
        post_tags_ids = post.tags.values_list('id', flat=True)  # получение айди тегов у текущего поста в виде списка
        # фильтрация постов у которых теги содержат полученные теги текущего (1+ совпадений)
        similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id) # исключить текущий пост из выборки
        # вычисляеться число общих тегов 
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags','-time_publish')[:4] # упорядочить рек. посты по убыванию кол-ва общих тегов и времени публикации 
        context['recommended_posts'] = similar_posts
        return context
    
    
class DeletePost(generic.DeleteView):
    template_name = 'delete.html'
    model = Post
    success_url = reverse_lazy('posts:list')
    
class UpdatePost(generic.UpdateView):
    template_name = 'update.html'
    model = Post
    fields = ['name', 'content', 'status', 'photo']
    
class CreateCommentView(generic.CreateView):
    model = Comment
    form_class = forms.CommentForm
    def is_ajax(self): # метод для проверки являеться ли полученный запрос ajax или нет
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get('post_id')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()
        
        try:
            if self.is_ajax():
                if self.request.user.is_authenticated:
                    data = {
                        'is_child': comment.is_child_node(),
                        'id': comment.id,
                        'author': comment.author.username,
                        'parent_id': comment.parent_id,
                        'time_create': comment.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                        'content': comment.content,
                        # 'author_avatar': comment.get_avatar
                    }
                    return JsonResponse(data, status = 200)
                else:
                    return JsonResponse(status = 403)
            else:
                return redirect(comment.post.get_absolute_url())
        except TemplateDoesNotExist:
            print(TemplateDoesNotExist)
            
    
    

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
    
class LikeAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] # Вернуть данные только если пользователь аутентифицирован
    def post(self, request, *args, **kwargs):
            obj_id = request.POST.get('object_id') # получить id текущего поста из запроса
            print(request.POST.get('object_id'))
            obj = self.get_object(obj_id)
            
            if request.user in obj.liked.all(): # если текущий пользователь уже лайкал пост
                obj.liked.remove(request.user) # удалить его из отношения
                data = {'likes_count': obj.liked.count(), 'is_liked': False} # сформированная дата для отправки на клиент
            else: # если пользователя нет в таблице отношений добавить его и сформировать другую дату
                obj.liked.add(request.user) 
                data = {'likes_count': obj.liked.count(), 'is_liked': True} 
            serializer = LikeSerializer(data) # сериализовать данные в json формат
            return Response(serializer.data) # вернуть на клиент сериализованные данные

    def get_object(obj_id):
        pass

        
class LikePostAPIView(LikeAPIView):
    def get_object(self, obj_id):
        return get_object_or_404(Post, id=obj_id)
    
class LikeCommentAPIView(LikeAPIView):
    def get_object(self, obj_id):
        return get_object_or_404(Comment, id=obj_id)
        
        

        