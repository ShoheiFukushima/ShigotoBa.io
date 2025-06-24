#!/bin/bash
# ダッシュボード起動スクリプト

echo "🚀 Publishing Dashboard 起動中..."

# 依存関係チェック
if ! command -v streamlit &> /dev/null; then
    echo "📦 Streamlitをインストール中..."
    pip install -r dashboard/requirements.txt
fi

# ダッシュボード起動
echo "✨ ダッシュボードを開いています..."
echo "ブラウザが自動で開かない場合は http://localhost:8501 にアクセスしてください"

cd /Users/fukushimashouhei/dev/marketing-automation-tools
streamlit run dashboard/app.py \
    --theme.base="dark" \
    --theme.primaryColor="#3b82f6" \
    --theme.backgroundColor="#0e1117" \
    --theme.secondaryBackgroundColor="#1a1f2e" \
    --server.port=8501 \
    --server.headless=false