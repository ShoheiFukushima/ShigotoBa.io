#!/usr/bin/env python3
"""
広告・マーケカテゴリページ
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="広告・マーケ",
    page_icon="🎨",
    layout="wide"
)

# ヘッダー
try:
    from components.header import render_header
    render_header()
except ImportError:
    pass

# サイドバー
try:
    from components.sidebar_simple import render_sidebar
    render_sidebar()
except ImportError:
    pass

st.title("🎨 広告・マーケ")

# メニューオプション
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎨 AI Creative Studio
    AIによるクリエイティブ生成
    """)
    if st.button("AI Creative Studioを開く", key="ai_creative", use_container_width=True):
        st.switch_page("pages/ai_creative_studio.py")

with col2:
    st.markdown("""
    ### ⚡ リアルタイム広告最適化
    広告パフォーマンスの最適化
    """)
    if st.button("広告最適化を開く", key="ad_optimizer", use_container_width=True):
        st.switch_page("pages/realtime_ad_optimizer.py")

with col3:
    st.markdown("""
    ### 💰 価格戦略コンサルティング
    価格設定の最適化
    """)
    if st.button("価格戦略を開く", key="pricing", use_container_width=True):
        st.switch_page("pages/pricing_strategy.py")

st.markdown("---")

# その他のツール
st.subheader("その他のマーケティングツール")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌐 マルチプラットフォーム管理", use_container_width=True):
        st.switch_page("pages/multi_platform_manager.py")
        
with col2:
    if st.button("🚀 自動投稿", use_container_width=True):
        st.switch_page("pages/auto_posting.py")
        
with col3:
    if st.button("📋 ツール一覧", use_container_width=True):
        st.switch_page("pages/marketing_tools_list.py")