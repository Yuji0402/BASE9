from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileEditForm
from .models import CustomUser


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'アカウントを作成しました。ようこそ、{user.username}さん！')
        return redirect('home')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        next_url = request.GET.get('next', 'home')
        return redirect(next_url)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')


def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    team = profile_user.get_team()
    match_posts = []
    recruit_posts = profile_user.recruit_posts.filter(is_active=True)[:5]
    if team:
        match_posts = team.match_posts.all()[:5]
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'team': team,
        'match_posts': match_posts,
        'recruit_posts': recruit_posts,
    })


@login_required
def profile_edit_view(request):
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'プロフィールを更新しました。')
        return redirect('profile', username=request.user.username)
    return render(request, 'accounts/profile_edit.html', {'form': form})
