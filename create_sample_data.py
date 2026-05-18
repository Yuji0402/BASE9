"""サンプルデータ作成スクリプト"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser
from teams.models import Team, TeamMembership
from matches.models import MatchPost
from recruitment.models import RecruitPost
from grounds.models import Ground
from datetime import date, timedelta

print("サンプルデータを作成中...")

# ユーザー作成
users_data = [
    ('yamada_taro', 'yamada@example.com', '東京都', '投手', '中級者'),
    ('sato_hanako', 'sato@example.com', '大阪府', '捕手', '初心者'),
    ('tanaka_ken', 'tanaka@example.com', '神奈川県', '遊撃手', '上級者'),
    ('suzuki_ai', 'suzuki@example.com', '埼玉県', '左翼手', '中級者'),
    ('ito_jiro', 'ito@example.com', '千葉県', '一塁手', '問わない'),
]

users = []
for username, email, pref, pos, level in users_data:
    user, created = CustomUser.objects.get_or_create(
        username=username,
        defaults={'email': email, 'prefecture': pref, 'position': pos, 'level': level}
    )
    if created:
        user.set_password('password123')
        user.save()
    users.append(user)
    print(f"  ユーザー: {username}")

# チーム作成
teams_data = [
    ('Victory FC', '東京都', '世田谷区', '毎週土曜・日曜に活動している草野球チームです。和気あいあいとした雰囲気で、初心者から経験者まで楽しめます！', '中級者', '土曜,日曜', True),
    ('大阪Braves', '大阪府', '梅田', '関西最強を目指す草野球チームです。真剣に野球に取り組みたい方大歓迎！', '上級者', '日曜,祝日', False),
    ('PEGASUS 18', '神奈川県', '横浜市', '横浜を拠点に活動しています。初心者歓迎！楽しく野球をやりましょう！', '初心者', '土曜', True),
    ('Samurai 27', '埼玉県', 'さいたま市', '埼玉のチームです。いつでも助っ人歓迎しています。', '中級者', '不定期', True),
    ('KANSAI BC', '兵庫県', '神戸市', '神戸発の草野球チーム。試合大好き！どんどん対戦申し込んでください。', '上級者', '土曜,日曜', False),
]

teams = []
for name, pref, city, desc, level, days, recruiting in teams_data:
    captain = users[len(teams) % len(users)]
    team, created = Team.objects.get_or_create(
        name=name,
        defaults={
            'description': desc, 'prefecture': pref, 'city': city,
            'level': level, 'activity_days': days, 'is_recruiting': recruiting,
            'captain': captain, 'members_count': 9,
        }
    )
    if created:
        TeamMembership.objects.get_or_create(team=team, user=captain, defaults={'role': 'captain'})
    teams.append(team)
    print(f"  チーム: {name}")

# 試合募集
matches_data = [
    ('【東京】来週土曜 対戦相手募集', teams[0], '東京都', '代々木公園野球場', date.today() + timedelta(days=7)),
    ('【大阪】練習試合しませんか？', teams[1], '大阪府', '鶴見緑地球技場', date.today() + timedelta(days=10)),
    ('【神奈川】初心者チームと試合したい！', teams[2], '神奈川県', '横浜山下公園グラウンド', date.today() + timedelta(days=14)),
    ('【埼玉】急募！来週日曜', teams[3], '埼玉県', '浦和駒場スタジアム', date.today() + timedelta(days=5)),
    ('【兵庫】5月の試合相手募集', teams[4], '兵庫県', '御崎公園球技場', date.today() + timedelta(days=20)),
    ('【東京】ゴールデンウィーク試合募集', teams[0], '東京都', '駒沢公園野球場', date.today() + timedelta(days=30)),
]

for title, team, pref, venue, dt in matches_data:
    post, created = MatchPost.objects.get_or_create(
        title=title,
        defaults={
            'team': team, 'prefecture': pref, 'venue': venue, 'date': dt,
            'level': team.level, 'innings': '7',
            'description': '詳細はチャットでご連絡ください！お気軽に申込みどうぞ。',
        }
    )
    if created:
        print(f"  試合募集: {title}")

# 助っ人・メンバー募集
recruits_data = [
    ('投手急募！来週の試合に助っ人を', 'helper', users[0], teams[0], '東京都', '投手'),
    ('メンバー募集！一緒に野球しよう', 'member', users[1], teams[2], '神奈川県', '問わない'),
    ('外野手の助っ人をお願いしたい', 'helper', users[2], teams[3], '埼玉県', '右翼手'),
    ('草野球チームを探しています', 'member', users[3], None, '大阪府', '二塁手'),
    ('初心者チームでゆるく野球したい', 'member', users[4], None, '千葉県', '問わない'),
]

for title, rtype, posted_by, team, pref, pos in recruits_data:
    post, created = RecruitPost.objects.get_or_create(
        title=title,
        defaults={
            'recruit_type': rtype, 'posted_by': posted_by, 'team': team,
            'prefecture': pref, 'position': pos, 'level': '問わない',
            'description': '詳細はメッセージでお気軽にどうぞ！',
        }
    )
    if created:
        print(f"  募集: {title}")

# グラウンド
grounds_data = [
    ('代々木公園野球場', '東京都渋谷区代々木神園町2-1', '東京都', '渋谷区', 35.6716, 139.6941, '土', '無料（許可証要）'),
    ('駒沢公園野球場', '東京都世田谷区駒沢公園1-1', '東京都', '世田谷区', 35.6204, 139.6681, '天然芝', '2,000円/時'),
    ('大阪城公園野球場', '大阪府大阪市中央区大阪城1-1', '大阪府', '大阪市', 34.6873, 135.5261, '土', '無料'),
    ('横浜山下公園グラウンド', '神奈川県横浜市中区山下町279', '神奈川県', '横浜市', 35.4422, 139.6466, '土', '無料'),
]

for name, address, pref, city, lat, lng, surface, fee in grounds_data:
    ground, created = Ground.objects.get_or_create(
        name=name,
        defaults={
            'address': address, 'prefecture': pref, 'city': city,
            'lat': lat, 'lng': lng, 'surface': surface, 'fee': fee,
            'added_by': users[0],
        }
    )
    if created:
        print(f"  グラウンド: {name}")

# 管理者ユーザー
admin_user, created = CustomUser.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@base9.jp', 'is_staff': True, 'is_superuser': True}
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("  管理者: admin / admin123")

print("\nサンプルデータ作成完了！")
print("管理者ログイン: admin / admin123")
print("テストユーザー: yamada_taro / password123")
