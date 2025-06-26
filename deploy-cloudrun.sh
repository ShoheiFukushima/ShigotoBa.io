#!/bin/bash

# 設定
PROJECT_ID="my-dashboard-463813"
SERVICE_NAME="shigotoba-io"
REGION="asia-northeast1"  # 東京リージョン
SECRET_NAME="gemini"  # 既存のシークレット

echo "🚀 Cloud Runへのデプロイを開始します..."

# 1. プロジェクトIDの確認
echo "プロジェクトID: $PROJECT_ID"
echo "サービス名: $SERVICE_NAME"
echo "リージョン: $REGION"
echo "シークレット: $SECRET_NAME"
read -p "これらの設定で続行しますか? (y/n): " confirm
if [[ $confirm != "y" ]]; then
    exit 1
fi

# 2. Google Cloudの設定
echo "📋 Google Cloudプロジェクトを設定中..."
gcloud config set project $PROJECT_ID

# 3. 必要なAPIを有効化
echo "🔧 必要なAPIを有効化中..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 4. Dockerイメージのビルドとプッシュ
echo "🏗️ Dockerイメージをビルド中..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# 5. Cloud Runにデプロイ
echo "🚀 Cloud Runにデプロイ中..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --set-env-vars "STREAMLIT_SERVER_HEADLESS=true" \
    --set-env-vars "STREAMLIT_SERVER_ADDRESS=0.0.0.0" \
    --set-env-vars "STREAMLIT_SERVER_PORT=8080" \
    --set-secrets "GEMINI_API_KEY=${SECRET_NAME}:latest"

# 6. サービスURLを取得
echo "✅ デプロイ完了！"
echo "サービスURL:"
gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'