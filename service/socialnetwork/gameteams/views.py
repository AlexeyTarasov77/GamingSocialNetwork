from django.shortcuts import redirect, render
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .models import Ad, Team

# Create your views here.
def index_view(request):
    return render(request, "gameteams/index.html")

class TeamListView(generic.ListView):
    template_name = "gameteams/team_list.html"
    queryset = Team.objects.only("name", "slug", "rating", "logo", "game", "country")
    context_object_name = "teams"

class AdCreateView(generic.CreateView, LoginRequiredMixin):
    template_name ="gameteams/ad_create.html"
    form_class = forms.AdCreateForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(self.request.user)
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        ad = form.save(commit=False)
        cd = form.cleaned_data
        print(cd)
        user = self.request.user
        ad.user = user
        if cd["type"] == "RECRUITING":
            ad.team = user.profile.team
        ad.save()
        messages.success(self.request, "Объявление успешно создано")
        return redirect(ad.get_absolute_url())
    
class TeamCreateView(generic.CreateView):
    template_name = "gameteams/team_create.html"
    form_class = forms.TeamCreateForm
    
    def form_valid(self, form):
        team = form.save(commit=False)
        user = self.request.user
        team.leader = team.founder = user
        team.save()
        messages.success(self.request, "Команда успешно создана")
        return redirect(team.get_absolute_url())
        
        
        