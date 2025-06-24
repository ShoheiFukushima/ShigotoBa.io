#!/usr/bin/env python3
"""
shigotoba.io - AI-Powered Marketing Automation Platform
メインエントリーポイント
"""

import streamlit as st
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="shigotoba.io - マーケティング自動化",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# デバッグ用
st.title("🚀 shigotoba.io")
st.markdown("AI-Powered Marketing Automation Platform")

# エラー情報
st.error("アプリケーションの起動に問題があります。修正中です...")

# デバッグ情報
with st.expander("デバッグ情報"):
    st.write("Current time:", datetime.now())
    st.write("Python path:", st.__file__)
    
# 手動リンク
st.markdown("---")
st.markdown("### 直接アクセス（テスト用）")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("[🏠 ホーム](/dashboard/home)")
    
with col2:
    st.markdown("[📊 プロジェクト管理](/dashboard/pages/project_management)")
    
with col3:
    st.markdown("[🎨 AI Creative Studio](/dashboard/pages/ai_creative_studio)")