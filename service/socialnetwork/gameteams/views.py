from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth import get_user_model
from . import forms
from .models import Ad, Team
from posts.mixins import ObjectViewsMixin
from .utils import TeamHandle
from users.models import Profile
User = get_user_model()

# Create your views here.
def index_view(request):
    return render(request, "gameteams/index.html")

class TeamListView(generic.ListView):
    template_name = "gameteams/teams/team_list.html"
    queryset = Team.objects.only("name", "slug", "rating", "logo", "game", "country")
    context_object_name = "teams"

    
class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "gameteams/teams/team_create.html"
    form_class = forms.TeamCreateForm
    
    def form_valid(self, form):
        team = form.save(commit=False)
        user = self.request.user
        team.leader = team.founder = user
        team.save()
        messages.success(self.request, "Команда успешно создана")
        return redirect(team.get_absolute_url())
    
class TeamDetailView(generic.DetailView):
    template_name = "gameteams/teams/team_detail.html"
    queryset = Team.objects.prefetch_related("members")
    context_object_name = "team"
    
def team_join_view(request, slug):
    team = Team.objects.get(slug=slug)
    user = request.user
    if user.profile.team:
        messages.error(request, "Вы уже состоите в команде")
        return JsonResponse({"msg": "Вы уже состоите в команде"}, status=400)
    handle = TeamHandle(team)
    req = handle.create_join_request(user)
    print(req)
    return JsonResponse({"msg": "Заявка на вступление отправлена"}, status=200)

class TeamJoinRequestsView(AccessMixin, generic.ListView):
    template_name = "gameteams/teams/team_join_requests.html"
    def get_queryset(self):
        tm = TeamHandle(self.team)
        return tm.get_all_join_requests()
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not request.user.is_authenticated or not user.profile.is_team_leader:
            return self.handle_no_permission()
        self.team = user.profile.team
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data)
        from_user_profile = get_object_or_404(Profile, user_id=data.get("from_user_id"))
        print(from_user_profile, from_user_profile.user_id)
        tm = TeamHandle(self.team)
        accepted = False
        if data.get("action") == "accept":
            tm.accept_join_request(from_user_profile)
            accepted = True
        elif data.get("action") == "decline":
            tm.remove_join_request(from_user_profile)
        return JsonResponse({"accepted": accepted})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.team
        return context

# ------- ADS -------
    
class AdListView(generic.ListView):
    paginate_by = 9
    context_object_name = "ads"
    template_name = "gameteams/ads/ad_list.html"
    queryset = Ad.objects.only("title", "content", "game", "type", "user")
    
    @staticmethod
    def __get_ad_type(ad_type):
        types = Ad.TYPE_CHOICES
        return list(types.keys())[list(types.values()).index(ad_type)]
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.method == "GET" and "type" in self.request.GET:
            queryset = queryset.filter(type=self.request.GET.get("type"))
        return queryset
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_type"] = self.__get_ad_type(Ad.TYPE_CHOICES["SEARCHING"])
        context["recruitment_type"] = self.__get_ad_type(Ad.TYPE_CHOICES["RECRUITING"])
        return context
    
    
class AdDetailView(ObjectViewsMixin, generic.DetailView):
    template_name = "gameteams/ads/ad_detail.html"
    queryset = Ad.objects.select_related("user")
    redis_key_prefix = "ads"
    
    
class AdCreateView(LoginRequiredMixin, generic.CreateView):
    template_name ="gameteams/ads/ad_create.html"
    form_class = forms.AdCreateForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        ad = form.save(commit=False)
        cd = form.cleaned_data
        user = self.request.user
        ad.user = user
        if cd["type"] == "RECRUITING":
            ad.team = user.profile.team
        ad.save()
        messages.success(self.request, "Объявление успешно создано")
        return redirect(ad.get_absolute_url())
    
    
def ad_bookmark_view(request, pk):
    ad = Ad.objects.get(pk=pk)
    user = request.user
    is_added = False
    if ad.favorites.filter(pk=user.pk).exists():
        ad.favorites.remove(user)
    else:
        ad.favorites.add(user)
        is_added = True
    return JsonResponse({"is_added": is_added}, status=200)
        
        