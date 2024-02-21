from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileUpdateForm
from django.db.utils import ProgrammingError, OperationalError
from django.db import IntegrityError

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
    
    
    

