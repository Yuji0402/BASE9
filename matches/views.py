from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import MatchPost, MatchApplication
from accounts.models import PREFECTURE_CHOICES, LEVEL_CHOICES


class MatchForm:
    pass


def _get_match_form():
    from django import forms
    from .models import MatchPost

    class MatchPostForm(forms.ModelForm):
        class Meta:
            model = MatchPost
            fields = ('title', 'description', 'date', 'start_time', 'prefecture',
                      'venue', 'level', 'innings')
            labels = {
                'title': 'タイトル', 'description': '詳細・コメント', 'date': '試合日',
                'start_time': '開始時間', 'prefecture': '都道府県', 'venue': 'グラウンド・場所',
                'level': '希望レベル', 'innings': 'イニング数',
            }
            widgets = {
                'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
                'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for name, field in self.fields.items():
                if name not in ('date', 'start_time', 'description'):
                    if isinstance(field.widget, __import__('django').forms.Select):
                        field.widget.attrs.update({'class': 'form-select'})
                    else:
                        field.widget.attrs.update({'class': 'form-control'})
    return MatchPostForm


class ApplicationForm:
    pass


def _get_app_form():
    from django import forms

    class AppForm(forms.Form):
        message = forms.CharField(
            label='メッセージ（任意）',
            widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            required=False
        )
    return AppForm


def match_list_view(request):
    posts = MatchPost.objects.filter(status='open')
    prefecture = request.GET.get('prefecture', '')
    level = request.GET.get('level', '')
    date_from = request.GET.get('date_from', '')
    q = request.GET.get('q', '')
    if prefecture:
        posts = posts.filter(prefecture=prefecture)
    if level:
        posts = posts.filter(level=level)
    if date_from:
        posts = posts.filter(date__gte=date_from)
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(venue__icontains=q))
    return render(request, 'matches/match_list.html', {
        'posts': posts,
        'prefecture_choices': PREFECTURE_CHOICES,
        'level_choices': LEVEL_CHOICES,
        'selected_prefecture': prefecture,
        'selected_level': level,
        'date_from': date_from,
        'q': q,
    })


def match_detail_view(request, pk):
    post = get_object_or_404(MatchPost, pk=pk)
    user_application = None
    user_team = None
    if request.user.is_authenticated:
        user_team = request.user.get_team()
        if user_team:
            user_application = post.applications.filter(applicant_team=user_team).first()
    AppForm = _get_app_form()
    form = AppForm()
    return render(request, 'matches/match_detail.html', {
        'post': post,
        'applications': post.applications.all(),
        'user_application': user_application,
        'user_team': user_team,
        'form': form,
    })


@login_required
def match_create_view(request):
    user_team = request.user.get_team()
    if not user_team:
        messages.warning(request, 'チームを作成してから試合募集を投稿できます。')
        return redirect('team-create')
    if request.user != user_team.captain:
        messages.warning(request, '試合募集はキャプテンのみ投稿できます。')
        return redirect('home')
    MatchPostForm = _get_match_form()
    form = MatchPostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.team = user_team
        post.save()
        messages.success(request, '試合募集を投稿しました！')
        return redirect('match-detail', pk=post.pk)
    return render(request, 'matches/match_form.html', {'form': form})


@login_required
def match_apply_view(request, pk):
    post = get_object_or_404(MatchPost, pk=pk, status='open')
    user_team = request.user.get_team()
    if not user_team:
        messages.warning(request, 'チームに所属してから申請できます。')
        return redirect('match-detail', pk=pk)
    if post.team == user_team:
        messages.warning(request, '自チームの募集には申請できません。')
        return redirect('match-detail', pk=pk)
    if post.applications.filter(applicant_team=user_team).exists():
        messages.info(request, 'すでに申請済みです。')
        return redirect('match-detail', pk=pk)
    AppForm = _get_app_form()
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
            MatchApplication.objects.create(
                post=post,
                applicant_team=user_team,
                message=form.cleaned_data['message']
            )
            messages.success(request, '申請しました！チャットで詳細を調整してください。')
            return redirect('match-detail', pk=pk)
    return redirect('match-detail', pk=pk)


@login_required
def match_application_action_view(request, pk, app_id, action):
    post = get_object_or_404(MatchPost, pk=pk, team__captain=request.user)
    app = get_object_or_404(MatchApplication, pk=app_id, post=post)
    if action == 'accept':
        app.status = 'accepted'
        app.save()
        post.status = 'confirmed'
        post.save()
        from chat.models import ChatRoom
        room, _ = ChatRoom.objects.get_or_create(
            match_post=post,
            defaults={'name': f'{post.title} チャット'}
        )
        room.participants.add(request.user, app.applicant_team.captain)
        messages.success(request, '申請を承認しました。チャットルームが作成されました。')
    elif action == 'reject':
        app.status = 'rejected'
        app.save()
        messages.success(request, '申請を却下しました。')
    return redirect('match-detail', pk=pk)
