from django.contrib.auth.models import AbstractUser
from django.db import models

PREFECTURE_CHOICES = [
    ('北海道', '北海道'), ('青森県', '青森県'), ('岩手県', '岩手県'), ('宮城県', '宮城県'),
    ('秋田県', '秋田県'), ('山形県', '山形県'), ('福島県', '福島県'), ('茨城県', '茨城県'),
    ('栃木県', '栃木県'), ('群馬県', '群馬県'), ('埼玉県', '埼玉県'), ('千葉県', '千葉県'),
    ('東京都', '東京都'), ('神奈川県', '神奈川県'), ('新潟県', '新潟県'), ('富山県', '富山県'),
    ('石川県', '石川県'), ('福井県', '福井県'), ('山梨県', '山梨県'), ('長野県', '長野県'),
    ('岐阜県', '岐阜県'), ('静岡県', '静岡県'), ('愛知県', '愛知県'), ('三重県', '三重県'),
    ('滋賀県', '滋賀県'), ('京都府', '京都府'), ('大阪府', '大阪府'), ('兵庫県', '兵庫県'),
    ('奈良県', '奈良県'), ('和歌山県', '和歌山県'), ('鳥取県', '鳥取県'), ('島根県', '島根県'),
    ('岡山県', '岡山県'), ('広島県', '広島県'), ('山口県', '山口県'), ('徳島県', '徳島県'),
    ('香川県', '香川県'), ('愛媛県', '愛媛県'), ('高知県', '高知県'), ('福岡県', '福岡県'),
    ('佐賀県', '佐賀県'), ('長崎県', '長崎県'), ('熊本県', '熊本県'), ('大分県', '大分県'),
    ('宮崎県', '宮崎県'), ('鹿児島県', '鹿児島県'), ('沖縄県', '沖縄県'),
]

POSITION_CHOICES = [
    ('投手', '投手（ピッチャー）'), ('捕手', '捕手（キャッチャー）'),
    ('一塁手', '一塁手（ファースト）'), ('二塁手', '二塁手（セカンド）'),
    ('三塁手', '三塁手（サード）'), ('遊撃手', '遊撃手（ショート）'),
    ('左翼手', '左翼手（レフト）'), ('中堅手', '中堅手（センター）'),
    ('右翼手', '右翼手（ライト）'), ('指名打者', '指名打者（DH）'),
    ('問わない', 'ポジション問わない'),
]

LEVEL_CHOICES = [
    ('初心者', '初心者'), ('中級者', '中級者'), ('上級者', '上級者'), ('問わない', 'レベル問わない'),
]


class CustomUser(AbstractUser):
    bio = models.TextField('自己紹介', blank=True)
    avatar = models.ImageField('アバター', upload_to='avatars/', blank=True, null=True)
    prefecture = models.CharField('都道府県', max_length=10, choices=PREFECTURE_CHOICES, blank=True)
    position = models.CharField('ポジション', max_length=10, choices=POSITION_CHOICES, blank=True)
    level = models.CharField('レベル', max_length=10, choices=LEVEL_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def get_team(self):
        membership = self.memberships.filter(role__in=['captain', 'member']).select_related('team').first()
        return membership.team if membership else None
