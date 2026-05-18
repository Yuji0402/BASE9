from django.db import models
from django.conf import settings
from accounts.models import PREFECTURE_CHOICES, LEVEL_CHOICES, POSITION_CHOICES

RECRUIT_TYPE_CHOICES = [
    ('helper', '助っ人募集'),
    ('member', 'メンバー募集'),
]

APPLICATION_STATUS_CHOICES = [
    ('pending', '申請中'),
    ('accepted', '承認'),
    ('rejected', '却下'),
]


class RecruitPost(models.Model):
    title = models.CharField('タイトル', max_length=100)
    description = models.TextField('詳細・コメント', blank=True)
    recruit_type = models.CharField('募集タイプ', max_length=10, choices=RECRUIT_TYPE_CHOICES)
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE,
        related_name='recruit_posts', verbose_name='募集チーム',
        null=True, blank=True
    )
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='recruit_posts', verbose_name='投稿者'
    )
    prefecture = models.CharField('都道府県', max_length=10, choices=PREFECTURE_CHOICES)
    position = models.CharField('希望ポジション', max_length=10, choices=POSITION_CHOICES, default='問わない')
    level = models.CharField('希望レベル', max_length=10, choices=LEVEL_CHOICES, default='問わない')
    date = models.DateField('希望日', blank=True, null=True)
    is_active = models.BooleanField('募集中', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_recruit_type_display()}] {self.title}'


class RecruitApplication(models.Model):
    post = models.ForeignKey(RecruitPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='recruit_applications', verbose_name='応募者'
    )
    message = models.TextField('メッセージ', blank=True)
    status = models.CharField('ステータス', max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'applicant')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.applicant.username} → {self.post.title}'
