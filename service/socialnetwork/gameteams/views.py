from typing import Any, Set

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from core.mixins import ObjectViewsMixin
from users.models import Profile

from . import forms
from .models import Ad, Game, Team
from gameteams.services.team_service import TeamService

User = get_user_model()


# Create your views here.
def index_view(request):
    return render(request, "gameteams/index.html")


class TeamListView(generic.ListView):
    """View for listing all teams"""

    template_name = "gameteams/teams/team_list.html"
    queryset = Team.objects.only(
        "name", "slug", "rating", "logo", "game", "country"
    ).select_related("game")
    context_object_name = "teams"
    current_game = None

    def get_queryset(self):
        queryset = super().get_queryset()
        country_code = self.request.GET.get("country")  # filtering by country
        game = self.request.GET.get("game")  # filtering by game
        query = {}
        if country_code:
            query["country"] = country_code
        if game:
            self.current_game = game
            query["game__slug"] = game
        return queryset.filter(**query)

    def _get_teams_countries(self):
        countries: Set = set()
        for team in self.object_list:
            if team.country not in countries:
                countries.add(team.country)
        return countries

    def _get_teams_games(self):
        return Game.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["games"] = self._get_teams_games()
        context["countries"] = self._get_teams_countries()
        context["current_game"] = self.current_game
        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    """View for creating a new team"""

    template_name = "gameteams/teams/team_create.html"
    form_class = forms.TeamCreateForm

    def form_valid(self, form):
        team = form.save(commit=False)
        user = self.request.user
        TeamService(team).create_leader_founder(user)
        messages.success(self.request, "Команда успешно создана")
        return redirect(team.get_absolute_url())


class TeamDetailView(generic.DetailView):
    """View for detailed information about a team"""

    template_name = "gameteams/teams/team_detail.html"
    queryset = Team.objects.prefetch_related("members").select_related("game")
    context_object_name = "team"


class TeamJoinView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        team_slug = self.kwargs.get("slug")
        team = Team.objects.get(slug=team_slug)
        user = request.user
        service = TeamService(team)
        if service.check_is_member(user.profile):
            return JsonResponse({"msg": "Вы уже состоите в команде"}, status=400)
        obj, created = service.create_join_request(user)
        msg = "Заявка на вступление отправлена"
        # if join req already existed - indicate that user already sent request
        if not created:
            msg = "Вы уже отправляли заявку на вступление"
        return JsonResponse({"msg": msg}, status=200)


@login_required
def leave_team_view(request, slug):
    team = get_object_or_404(Team, slug=slug)
    leaving_member = request.user.profile
    if leaving_member in team.members.all():
        service = TeamService(team)
        service.remove_member(leaving_member)
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse(
            {"success": False, "error_msg": "Вы не состоите в этой команде"}, status=404
        )


@login_required
def remove_team_member_view(request, pk):
    member = get_object_or_404(Profile, pk=pk)
    team = request.user.profile.team
    print(team, request.user)
    if not team or not request.user == team.leader:
        return JsonResponse(
            {"success": False, "error_msg": "Недостаточно прав"}, status=403
        )
    if member not in team.members.all():
        return JsonResponse(
            {"success": False, "error_msg": "Участник не состоит в вашей команде"},
            status=404,
        )
    service = TeamService(team)
    service.remove_member(member)
    return JsonResponse({"success": True}, status=200)


@login_required
def make_team_leader_view(request, pk):
    member = get_object_or_404(Profile, pk=pk)
    team = member.team
    if not request.user == team.leader:
        return JsonResponse({"success": False}, status=403)
    service = TeamService(team)
    service.make_leader(member.user)
    messages.success(
        request, f"Участник {member.user.username} стал лидером команды {team.name}"
    )
    return redirect(team.get_absolute_url())


@login_required
def team_handle_view(request, slug):
    team = get_object_or_404(Team, slug=slug)
    if not request.user == team.leader:
        return HttpResponse("Недостаточно прав", status=403)
    return render(
        request,
        "gameteams/teams/team_handle.html",
        {"team": team, "team_members": team.members.exclude(user_id=team.leader.id)},
    )


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
        print(from_user_profile, from_user_profile.user_id)
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

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request") == "true":
            return ["gameteams/ads/ad_list_hx.html"]
        return super().get_template_names()

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.method == "GET" and (ad_type := self.request.GET.get("type")):
            queryset = queryset.filter(type=ad_type)
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add ad-types names to context for using in query params."""
        context = super().get_context_data(**kwargs)
        # passing to context names of get param's value for ads filtering (?type=RECRUITING)
        context["search_type"] = "SEARCHING"
        context["recruitment_type"] = "RECRUITING"
        return context


class AdDetailView(ObjectViewsMixin, generic.DetailView):
    """View for detailed information about ad"""

    template_name = "gameteams/ads/ad_detail.html"
    queryset = Ad.objects.select_related("user")
    redis_key_prefix = "ads"


class AdCreateView(LoginRequiredMixin, generic.CreateView):
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
