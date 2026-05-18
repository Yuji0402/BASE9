# BASE9 - 草野球マッチングアプリ

草野球チーム同士が簡単に試合相手を見つけられるマッチングサービス。

## 機能
- 試合相手マッチング（募集・申請・承認）
- 助っ人・メンバー募集
- リアルタイムチャット（Django Channels + WebSocket）
- グラウンド情報（OpenStreetMap + Leaflet.js）
- ユーザー・チーム管理

## ローカル起動

```bash
# 仮想環境を有効化
source venv/bin/activate

# 開発サーバー起動
python manage.py runserver
```

http://127.0.0.1:8000 にアクセス

## テストアカウント
- 管理者: admin / admin123
- テストユーザー: yamada_taro / password123

## デプロイ（Render）
1. GitHubにプッシュ
2. RenderでNew Web Service
3. Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Start Command: Procfile参照
5. 環境変数を.env.exampleを参考に設定
