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
from gameteams.services.team_service import TeamService
from users.models import Profile

User = get_user_model()


# Create your views here.
def index_view(request):
    return render(request, "gameteams/index.html")


class TeamListView(generic.ListView):
    """View for listing all teams"""

    template_name = "gameteams/teams/team_list.html"
    queryset = Team.objects.only("name", "slug", "rating", "logo", "game", "country")
    context_object_name = "teams"


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    """View for creating a new team"""

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
    """View for detailed information about a team"""

    template_name = "gameteams/teams/team_detail.html"
    queryset = Team.objects.prefetch_related("members")
    context_object_name = "team"


def team_join_view(request, slug):
    """View for sending a join request to a team"""
    team = Team.objects.get(slug=slug)
    user = request.user
    if user.profile.team:
        messages.error(request, "Вы уже состоите в команде")
        return JsonResponse({"msg": "Вы уже состоите в команде"}, status=400)
    service = TeamService(team)
    service.create_join_request(user)
    return JsonResponse({"msg": "Заявка на вступление отправлена"}, status=200)


class TeamJoinRequestsView(AccessMixin, generic.ListView):
    """View for listing all join requests to a team.
    Accept and decline join requests with POST request.
    """

    template_name = "gameteams/teams/team_join_requests.html"

    def get_queryset(self):
        service = TeamService(self.team)
        return service.get_all_join_requests()

    def dispatch(self, request, *args, **kwargs):
        """Checks that user is authenticated and is a team leader"""
        user = request.user
        if not request.user.is_authenticated or not user.profile.is_team_leader:
            return self.handle_no_permission()
        self.team = user.profile.team
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Accepting/Declining incoming join requests"""
        data = request.POST
        from_user_profile = get_object_or_404(Profile, user_id=data.get("from_user_id"))
        service = TeamService(self.team)
        accepted = False
        if data.get("action") == "accept":
            service.accept_join_request(from_user_profile)
            accepted = True
        elif data.get("action") == "decline":
            service.remove_join_request(from_user_profile)
        return JsonResponse({"accepted": accepted})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.team
        return context


# ------- ADS -------


class AdListView(generic.ListView):
    """View for listing all ads.
    Filter ads by their type provided in query params.
    """

    paginate_by = 9
    context_object_name = "ads"
    template_name = "gameteams/ads/ad_list.html"
    queryset = Ad.objects.only("title", "content", "game", "type", "user")

    @staticmethod
    def __get_ad_type(ad_type):
        """Get key name by value"""
        types = Ad.TYPE_CHOICES
        return list(types.keys())[list(types.values()).index(ad_type)]

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        # filter by ad type
        if self.request.method == "GET" and "type" in self.request.GET:
            queryset = queryset.filter(type=self.request.GET.get("type"))
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add ad-types names to context for using in query params."""
        context = super().get_context_data(**kwargs)
        context["search_type"] = self.__get_ad_type(Ad.TYPE_CHOICES["SEARCHING"])
        context["recruitment_type"] = self.__get_ad_type(Ad.TYPE_CHOICES["RECRUITING"])
        return context


class AdDetailView(ObjectViewsMixin, generic.DetailView):
    """View for detailed information about ad"""
    template_name = "gameteams/ads/ad_detail.html"
    queryset = Ad.objects.select_related("user")
    redis_key_prefix = "ads"


class AdCreateView(LoginRequiredMixin, generic.CreateView):
    """View for creating new ad"""
    template_name = "gameteams/ads/ad_create.html"
    form_class = forms.AdCreateForm

    def get_form_kwargs(self):
        """Passes current user to form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Saving new add, adding some additional data."""
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
    """set/unset ad bookmark"""
    ad = Ad.objects.get(pk=pk)
    user = request.user
    is_added = False
    if ad.favorites.filter(pk=user.pk).exists():
        ad.favorites.remove(user)
    else:
        ad.favorites.add(user)
        is_added = True
    return JsonResponse({"is_added": is_added}, status=200)
