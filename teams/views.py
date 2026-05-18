from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Team, TeamMembership
from .forms import TeamForm
from accounts.models import PREFECTURE_CHOICES


def team_list_view(request):
    teams = Team.objects.all()
    prefecture = request.GET.get('prefecture', '')
    level = request.GET.get('level', '')
    recruiting = request.GET.get('recruiting', '')
    q = request.GET.get('q', '')
    if prefecture:
        teams = teams.filter(prefecture=prefecture)
    if level:
        teams = teams.filter(level=level)
    if recruiting:
        teams = teams.filter(is_recruiting=True)
    if q:
        teams = teams.filter(Q(name__icontains=q) | Q(description__icontains=q))
    return render(request, 'teams/team_list.html', {
        'teams': teams,
        'prefecture_choices': PREFECTURE_CHOICES,
        'selected_prefecture': prefecture,
        'selected_level': level,
        'selected_recruiting': recruiting,
        'q': q,
    })


def team_detail_view(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = team.memberships.filter(role__in=['captain', 'member']).select_related('user')
    user_membership = None
    if request.user.is_authenticated:
        user_membership = team.memberships.filter(user=request.user).first()
    match_posts = team.match_posts.filter(status='open')[:5]
    return render(request, 'teams/team_detail.html', {
        'team': team,
        'members': members,
        'user_membership': user_membership,
        'match_posts': match_posts,
    })


@login_required
def team_create_view(request):
    if TeamMembership.objects.filter(user=request.user, role__in=['captain', 'member']).exists():
        messages.warning(request, 'すでにチームに所属しています。')
        return redirect('home')
    form = TeamForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        team = form.save(commit=False)
        team.captain = request.user
        team.save()
        TeamMembership.objects.create(team=team, user=request.user, role='captain')
        messages.success(request, f'チーム「{team.name}」を作成しました！')
        return redirect('team-detail', pk=team.pk)
    return render(request, 'teams/team_form.html', {'form': form, 'is_create': True})


@login_required
def team_edit_view(request, pk):
    team = get_object_or_404(Team, pk=pk, captain=request.user)
    form = TeamForm(request.POST or None, request.FILES or None, instance=team)
    if form.is_valid():
        form.save()
        messages.success(request, 'チーム情報を更新しました。')
        return redirect('team-detail', pk=team.pk)
    return render(request, 'teams/team_form.html', {'form': form, 'team': team, 'is_create': False})


@login_required
def team_join_view(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if team.memberships.filter(user=request.user).exists():
        messages.info(request, 'すでに申請済みまたはメンバーです。')
        return redirect('team-detail', pk=pk)
    TeamMembership.objects.create(team=team, user=request.user, role='pending')
    messages.success(request, f'「{team.name}」に参加申請しました。')
    return redirect('team-detail', pk=pk)


@login_required
def membership_action_view(request, pk, user_id, action):
    team = get_object_or_404(Team, pk=pk, captain=request.user)
    membership = get_object_or_404(TeamMembership, team=team, user_id=user_id)
    if action == 'approve':
        membership.role = 'member'
        membership.save()
        messages.success(request, 'メンバーを承認しました。')
    elif action == 'reject':
        membership.delete()
        messages.success(request, '申請を却下しました。')
    return redirect('team-detail', pk=pk)
