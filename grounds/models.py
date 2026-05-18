from django.db import models
from django.conf import settings
from accounts.models import PREFECTURE_CHOICES

SURFACE_CHOICES = [
    ('土', '土'),
    ('天然芝', '天然芝'),
    ('人工芝', '人工芝'),
    ('その他', 'その他'),
]


class Ground(models.Model):
    name = models.CharField('グラウンド名', max_length=100)
    address = models.CharField('住所', max_length=200)
    prefecture = models.CharField('都道府県', max_length=10, choices=PREFECTURE_CHOICES)
    city = models.CharField('市区町村', max_length=50, blank=True)
    lat = models.DecimalField('緯度', max_digits=10, decimal_places=7, null=True, blank=True)
    lng = models.DecimalField('経度', max_digits=10, decimal_places=7, null=True, blank=True)
    description = models.TextField('説明・備考', blank=True)
    surface = models.CharField('グラウンド種別', max_length=10, choices=SURFACE_CHOICES, default='土')
    capacity = models.PositiveIntegerField('収容人数', blank=True, null=True)
    fee = models.CharField('使用料', max_length=100, blank=True)
    phone = models.CharField('電話番号', max_length=20, blank=True)
    website = models.URLField('公式サイト', blank=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='added_grounds', verbose_name='登録者'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['prefecture', 'name']

    def __str__(self):
        return f'{self.name} ({self.prefecture})'


class GroundReservation(models.Model):
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE, related_name='reservations')
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE,
        related_name='ground_reservations', verbose_name='予約チーム'
    )
    date = models.DateField('予約日')
    start_time = models.TimeField('開始時間')
    end_time = models.TimeField('終了時間')
    is_shared = models.BooleanField('グラウンドをシェア可能', default=False)
    note = models.TextField('備考', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.ground.name} - {self.team.name} ({self.date})'
