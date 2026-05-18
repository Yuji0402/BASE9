from django.db import models
from django.conf import settings
from accounts.models import PREFECTURE_CHOICES, LEVEL_CHOICES

MATCH_STATUS_CHOICES = [
    ('open', '募集中'),
    ('confirmed', '対戦相手確定'),
    ('closed', '終了'),
]

APPLICATION_STATUS_CHOICES = [
    ('pending', '申請中'),
    ('accepted', '承認'),
    ('rejected', '却下'),
]

INNING_CHOICES = [(str(i), f'{i}イニング') for i in range(3, 10)]


class MatchPost(models.Model):
    title = models.CharField('タイトル', max_length=100)
    description = models.TextField('詳細・コメント', blank=True)
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE,
        related_name='match_posts', verbose_name='投稿チーム'
    )
    date = models.DateField('試合日')
    start_time = models.TimeField('開始時間', blank=True, null=True)
    prefecture = models.CharField('都道府県', max_length=10, choices=PREFECTURE_CHOICES)
    venue = models.CharField('グラウンド・場所', max_length=200, blank=True)
    level = models.CharField('希望レベル', max_length=10, choices=LEVEL_CHOICES, default='問わない')
    innings = models.CharField('イニング数', max_length=2, choices=INNING_CHOICES, default='7')
    status = models.CharField('ステータス', max_length=10, choices=MATCH_STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', '-created_at']

    def __str__(self):
        return f'{self.title} ({self.date})'


class MatchApplication(models.Model):
    post = models.ForeignKey(MatchPost, on_delete=models.CASCADE, related_name='applications')
    applicant_team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE,
        related_name='match_applications', verbose_name='申請チーム'
    )
    message = models.TextField('メッセージ', blank=True)
    status = models.CharField('ステータス', max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'applicant_team')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.applicant_team.name} → {self.post.title}'
