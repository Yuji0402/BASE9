# BASE9 - 草野球マッチングアプリ

## プロジェクト概要
草野球チーム同士が試合相手・助っ人・メンバーを見つけられるマッチングサービス。

## 技術スタック
- **Backend:** Python 3.14 / Django 6.0.5
- **WebSocket:** Django Channels 4.x（リアルタイムチャット）
- **Frontend:** Bootstrap 5 / Leaflet.js（OpenStreetMap）/ Vanilla JS
- **DB:** SQLite（開発）→ MySQL（本番予定）
- **静的ファイル:** WhiteNoise
- **デプロイ先:** Render（Procfileで設定済み）

## ディレクトリ構成
```
BASE9/
├── accounts/      # ユーザー認証・プロフィール
├── teams/         # チーム管理
├── matches/       # 試合マッチング
├── recruitment/   # 助っ人・メンバー募集
├── chat/          # リアルタイムチャット（WebSocket）
├── grounds/       # グラウンド情報・地図
├── config/        # Django設定・URL・ASGI
├── static/        # CSS・画像・SVGロゴ
├── templates/     # HTMLテンプレート
└── create_sample_data.py  # サンプルデータ投入スクリプト
```

## よく使うコマンド
```bash
# 仮想環境を有効化（必須）
source venv/bin/activate

# 開発サーバー起動
python manage.py runserver

# マイグレーション
python manage.py makemigrations
python manage.py migrate

# サンプルデータ投入
python manage.py shell < create_sample_data.py  # または
python create_sample_data.py

# 静的ファイル収集（本番用）
python manage.py collectstatic
```

## テストアカウント
| ユーザー | パスワード | 権限 |
|---|---|---|
| admin | admin123 | 管理者 |
| yamada_taro | password123 | 一般（Victory FCキャプテン） |
| sato_hanako | password123 | 一般（大阪Braves） |

## デザイン
- **テーマカラー:** 青（`#1D4ED8` primary、`#3B82F6` light）
- **コンセプト:** Wantedlyのようなシンプル・洗練されたデザイン
- **ロゴ:** `static/img/logo.svg`（野球ボール＋太陽アイコン、青）
- **ヒーロー画像:** `static/img/hero-baseball.jpg`

## 主要モデル
- `accounts.CustomUser` - カスタムユーザー（都道府県・ポジション・レベル）
- `teams.Team` / `teams.TeamMembership` - チームとメンバー管理
- `matches.MatchPost` / `matches.MatchApplication` - 試合募集と申請
- `recruitment.RecruitPost` / `recruitment.RecruitApplication` - 助っ人・メンバー募集
- `chat.ChatRoom` / `chat.Message` - チャットルームとメッセージ
- `grounds.Ground` / `grounds.GroundReservation` - グラウンドと予約情報

## チャット（WebSocket）
- `chat/consumers.py` - WebSocket処理
- `chat/routing.py` - WebSocketルーティング
- `config/asgi.py` - ASGIアプリ設定
- 開発環境: `InMemoryChannelLayer`
- 本番環境: Redisに切り替え要（`channels_redis`）

## GitHub
https://github.com/Yuji0402/BASE9.git

## デプロイ（Render）
- Build: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
- Start: `daphne -b 0.0.0.0 -p $PORT config.asgi:application`
- 環境変数: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`
