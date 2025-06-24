#!/bin/bash
# ダッシュボード起動スクリプト（簡易版）

echo "🚀 Publishing Dashboard を起動します..."

# Streamlitのパス
STREAMLIT_PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin/streamlit"

# 環境変数設定（メール通知をスキップ）
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# ダッシュボード起動
cd /Users/fukushimashouhei/dev/marketing-automation-tools
$STREAMLIT_PATH run dashboard/app.py --server.port=8501 --server.headless=true

echo "ブラウザで http://localhost:8501 を開いてください"