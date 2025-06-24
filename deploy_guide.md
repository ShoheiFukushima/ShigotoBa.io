# 🚀 マーケティング自動化ツール デプロイガイド

## 📱 デプロイオプション

### 1. **Streamlit Cloud（推奨・無料）**
最も簡単で、スマホからもアクセス可能

#### 必要なもの:
- GitHubアカウント
- Streamlit Cloudアカウント（無料）

#### 手順:
1. GitHubにコードをプッシュ
2. Streamlit Cloudでアプリを作成
3. 環境変数を設定
4. デプロイ完了！

### 2. **Vercel（高速・無料枠あり）**
Next.jsアプリとして変換してデプロイ

### 3. **Google Cloud Run（スケーラブル）**
Dockerコンテナとしてデプロイ

### 4. **Heroku（簡単・有料）**
簡単なデプロイが可能

---

## 🎯 Streamlit Cloudへのデプロイ手順

### Step 1: GitHubリポジトリの準備

```bash
# リポジトリの初期化
cd /Users/fukushimashouhei/dev/marketing-automation-tools
git init

# .gitignoreの確認
cat .gitignore

# ファイルの追加
git add .
git commit -m "Initial commit: Marketing Automation Tools"

# GitHubでリポジトリを作成後
git remote add origin https://github.com/YOUR_USERNAME/marketing-automation-tools.git
git branch -M main
git push -u origin main
```

### Step 2: requirements.txtの作成

```txt
streamlit==1.32.0
pandas==2.2.0
plotly==5.19.0
google-generativeai==0.8.5
python-dotenv==1.0.0
beautifulsoup4==4.12.0
requests==2.31.0
schedule==1.2.0
asyncio==3.4.3
```

### Step 3: Streamlit Cloudでデプロイ

1. https://streamlit.io/cloud にアクセス
2. GitHubでサインイン
3. "New app"をクリック
4. リポジトリを選択
5. メインファイルパス: `dashboard/home.py`
6. 環境変数を設定（Secrets）

### Step 4: 環境変数の設定

Streamlit CloudのSecretsに以下を追加:

```toml
# .streamlit/secrets.toml の内容
GOOGLE_API_KEY = "AIzaSyCI1pC2rKIiq-KXuxItSCvsYt2rcrx0Ye4"
GEMINI_API_KEY = "AIzaSyCI1pC2rKIiq-KXuxItSCvsYt2rcrx0Ye4"

[feature_flags]
ENABLE_AI_CHAT = true
ENABLE_SOCIAL_POSTING = false
```

---

## 📱 スマホアクセス設定

### デプロイ後:
1. **URL共有**: `https://YOUR-APP-NAME.streamlit.app`
2. **QRコード生成**: URLからQRコードを生成
3. **PWA対応**: スマホのホーム画面に追加可能

### スマホ最適化:
- レスポンシブデザイン対応済み
- タッチ操作最適化
- モバイルビュー自動調整

---

## 🐳 Docker デプロイ（オプション）

### Dockerfile作成:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/home.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### docker-compose.yml:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - .:/app
```

---

## 🔧 デプロイ前チェックリスト

- [ ] .envファイルが.gitignoreに含まれている
- [ ] requirements.txtが最新
- [ ] 不要なファイルの削除
- [ ] READMEの作成
- [ ] ライセンスの設定

---

## 🎉 デプロイ完了後

1. **アクセステスト**: PC/スマホ両方から確認
2. **パフォーマンス確認**: 読み込み速度チェック
3. **機能テスト**: 各機能の動作確認
4. **共有**: URLをQRコードで共有

スマホからいつでもマーケティング自動化ツールにアクセス可能に！