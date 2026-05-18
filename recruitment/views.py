from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import RecruitPost, RecruitApplication
from accounts.models import PREFECTURE_CHOICES, LEVEL_CHOICES, POSITION_CHOICES


def _get_recruit_form():
    from django import forms
    from .models import RecruitPost

    class RecruitPostForm(forms.ModelForm):
        class Meta:
            model = RecruitPost
            fields = ('title', 'description', 'recruit_type', 'prefecture',
                      'position', 'level', 'date')
            labels = {
                'title': 'タイトル', 'description': '詳細', 'recruit_type': '募集タイプ',
                'prefecture': '都道府県', 'position': '希望ポジション',
                'level': '希望レベル', 'date': '希望日（任意）',
            }
            widgets = {
                'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for name, field in self.fields.items():
                if name not in ('date', 'description'):
                    if isinstance(field.widget, __import__('django').forms.Select):
                        field.widget.attrs.update({'class': 'form-select'})
                    else:
                        field.widget.attrs.update({'class': 'form-control'})
    return RecruitPostForm


def recruitment_list_view(request):
    posts = RecruitPost.objects.filter(is_active=True)
    recruit_type = request.GET.get('type', '')
    prefecture = request.GET.get('prefecture', '')
    q = request.GET.get('q', '')
    if recruit_type:
        posts = posts.filter(recruit_type=recruit_type)
    if prefecture:
        posts = posts.filter(prefecture=prefecture)
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request, 'recruitment/recruit_list.html', {
        'posts': posts,
        'prefecture_choices': PREFECTURE_CHOICES,
        'selected_type': recruit_type,
        'selected_prefecture': prefecture,
        'q': q,
    })


def recruitment_detail_view(request, pk):
    post = get_object_or_404(RecruitPost, pk=pk)
    user_application = None
    if request.user.is_authenticated:
        user_application = post.applications.filter(applicant=request.user).first()
    return render(request, 'recruitment/recruit_detail.html', {
        'post': post,
        'applications': post.applications.all() if request.user == post.posted_by else None,
        'user_application': user_application,
    })


@login_required
def recruitment_create_view(request):
    RecruitPostForm = _get_recruit_form()
    form = RecruitPostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.posted_by = request.user
        team = request.user.get_team()
        if team and post.recruit_type == 'helper':
            post.team = team
        post.save()
        messages.success(request, '募集を投稿しました！')
        return redirect('recruitment-detail', pk=post.pk)
    return render(request, 'recruitment/recruit_form.html', {'form': form})


@login_required
def recruitment_apply_view(request, pk):
    post = get_object_or_404(RecruitPost, pk=pk, is_active=True)
    if post.posted_by == request.user:
        messages.warning(request, '自分の投稿には応募できません。')
        return redirect('recruitment-detail', pk=pk)
    if post.applications.filter(applicant=request.user).exists():
        messages.info(request, 'すでに応募済みです。')
        return redirect('recruitment-detail', pk=pk)
    if request.method == 'POST':
        message = request.POST.get('message', '')
        RecruitApplication.objects.create(post=post, applicant=request.user, message=message)
        messages.success(request, '応募しました！')
    return redirect('recruitment-detail', pk=pk)


@login_required
def recruitment_application_action_view(request, pk, app_id, action):
    post = get_object_or_404(RecruitPost, pk=pk, posted_by=request.user)
    app = get_object_or_404(RecruitApplication, pk=app_id, post=post)
    if action == 'accept':
        app.status = 'accepted'
        app.save()
        from chat.models import ChatRoom
        room, _ = ChatRoom.objects.get_or_create(
            recruit_post=post,
            defaults={'name': f'{post.title} チャット'}
        )
        room.participants.add(request.user, app.applicant)
        messages.success(request, '応募を承認しました。チャットで詳細を調整してください。')
    elif action == 'reject':
        app.status = 'rejected'
        app.save()
        messages.success(request, '応募を却下しました。')
    return redirect('recruitment-detail', pk=pk)
