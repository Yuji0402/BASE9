from django.db import models
from django.conf import settings
from accounts.models import PREFECTURE_CHOICES, LEVEL_CHOICES

ACTIVITY_DAY_CHOICES = [
    ('月曜', '月曜'), ('火曜', '火曜'), ('水曜', '水曜'), ('木曜', '木曜'),
    ('金曜', '金曜'), ('土曜', '土曜'), ('日曜', '日曜'), ('祝日', '祝日'),
    ('不定期', '不定期'),
]

MEMBER_ROLE_CHOICES = [
    ('captain', 'キャプテン'),
    ('member', 'メンバー'),
    ('pending', '承認待ち'),
]


class Team(models.Model):
    name = models.CharField('チーム名', max_length=100)
    description = models.TextField('チーム紹介')
    prefecture = models.CharField('都道府県', max_length=10, choices=PREFECTURE_CHOICES)
    city = models.CharField('市区町村', max_length=50, blank=True)
    level = models.CharField('レベル', max_length=10, choices=LEVEL_CHOICES, default='問わない')
    activity_days = models.CharField('活動曜日', max_length=100, blank=True)
    members_count = models.PositiveIntegerField('現在のメンバー数', default=1)
    image = models.ImageField('チーム画像', upload_to='teams/', blank=True, null=True)
    captain = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='captained_teams', verbose_name='代表者'
    )
    is_recruiting = models.BooleanField('メンバー募集中', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_member_count(self):
        return self.memberships.filter(role__in=['captain', 'member']).count()


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships'
    )
    role = models.CharField('役割', max_length=10, choices=MEMBER_ROLE_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.team.name} ({self.role})'
