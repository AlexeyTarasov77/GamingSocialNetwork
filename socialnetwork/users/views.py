from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.db.utils import ProgrammingError, OperationalError
from django.db import IntegrityError

# Create your views here.
class ProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Profile, user=self.request.user)
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
    
    
    
    

