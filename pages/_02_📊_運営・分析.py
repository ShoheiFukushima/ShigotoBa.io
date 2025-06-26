#!/usr/bin/env python3
"""
運営・分析カテゴリページ
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="運営・分析",
    page_icon="📊",
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

st.title("📊 運営・分析")

# メニューオプション
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📈 パフォーマンスダッシュボード
    KPIとメトリクスの監視
    """)
    if st.button("ダッシュボードを開く", key="perf_dash", use_container_width=True):
        st.switch_page("pages/performance_dashboard.py")

with col2:
    st.markdown("""
    ### 🎯 アトリビューション分析
    マーケティング効果の測定
    """)
    if st.button("アトリビューション分析を開く", key="attr_analysis", use_container_width=True):
        st.switch_page("pages/attribution_analysis.py")

with col3:
    st.markdown("""
    ### 🛤️ カスタマージャーニー
    顧客行動の可視化
    """)
    if st.button("カスタマージャーニーを開く", key="cust_journey", use_container_width=True):
        st.switch_page("pages/customer_journey_engine.py")

st.markdown("---")

# その他のツール
st.subheader("その他の分析ツール")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 プロダクト分析", use_container_width=True):
        st.switch_page("pages/product_analysis.py")
        
with col2:
    if st.button("💬 リアルタイムAIチャット", use_container_width=True):
        st.switch_page("pages/realtime_chat.py")
        
with col3:
    if st.button("📋 ツール一覧", use_container_width=True):
        st.switch_page("pages/analysis_tools_list.py")