from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileUpdateForm
from django.db.utils import ProgrammingError, OperationalError
from django.db import IntegrityError
from django.contrib import messages
from rest_framework import generics
from .serializers import SubscribeSerializer
from rest_framework.response import Response

# Create your views here.
class ProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Profile, user_slug=self.kwargs.get('username', None))
    def post(self, request, *args, **kwargs):
        if request.FILES['image']:
        # try:
            print(request.FILES)
            instance = self.get_object()
            instance.image = request.FILES['image']
            instance.save()
            return JsonResponse({'path': instance.image.url})
        # except [ProgrammingError, OperationalError, IntegrityError] as error:
        #     return JsonResponse({'error': error}, status=500)
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['is_owner'] = True if self.get_object().user == self.request.user else False
        return context
        
    
    
def profile_middleware(request):
    if request.user.is_authenticated:
        return redirect(request.user.profile_user.get_absolute_url())
    else: 
        return redirect("account_login")

class ProfileUpdateView(generic.UpdateView):
    slug_url_kwarg = 'username'
    slug_field = 'user_slug'
    template_name = 'users/profile_update.html'
    model = Profile
    form_class = ProfileUpdateForm
    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)
    

class SubscribeAPIView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = SubscribeSerializer
    lookup_field = 'user_slug'
    lookup_url_kwarg = 'username'

    def get(self, request, username):
        user_profile = self.get_object()
        if request.user in user_profile.followers.all():
            return Response({'is_subscribed': True})
        else:
            return Response({'is_subscribed': False})
        
    def patch(self, request, username): 
        user_profile = self.get_object() # получение профиля пользователя на которого подписываются
        user = request.user # получение текущего пользователя который хочеть подписаться/отписаться
        if user in user_profile.followers.all(): # если пользователь уже подписан
            user_profile.followers.remove(user) # отписаться
            user.profile_following.remove(user_profile.user) # удалить из подписок пользователя от которого отписываемся
            return Response({'is_subscribed': False})
        else:  # если пользователь еще не подписан
            user_profile.followers.add(request.user) # подписаться
            user.profile_following.add(user_profile.user) # добавить в подписки пользователя на которого подписываемся
            return Response({'is_subscribed': True})
    
    

