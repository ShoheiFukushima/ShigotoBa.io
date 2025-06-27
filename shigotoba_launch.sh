#!/bin/bash
# Shigotoba.io 起動スクリプト

echo "🏭 Shigotoba.io 起動スクリプト"
echo "================================"

# 環境チェック
echo "✅ 環境チェック中..."

# Pythonバージョン確認
python_version=$(python --version 2>&1)
echo "   Python: $python_version"

# Streamlitインストール確認
if python -c "import streamlit" 2>/dev/null; then
    echo "   Streamlit: ✅ インストール済み"
else
    echo "   Streamlit: ❌ 未インストール"
    echo "   pip install streamlit を実行してください"
    exit 1
fi

# APIキー確認（オプション）
if [ -f .env ]; then
    echo "   .env: ✅ 設定ファイル存在"
else
    echo "   .env: ⚠️  設定ファイルなし（AIモジュールを使用する場合は設定が必要）"
fi

echo ""
echo "🚀 Shigotoba.ioを起動します..."
echo "================================"
echo ""

# Streamlitアプリを起動
streamlit run app_shigotoba.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false \
    --theme.base light

echo ""
echo "✨ Shigotoba.ioが終了しました"