#!/usr/bin/env python3
"""
新規開発カテゴリページ
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="新規開発",
    page_icon="🏗️",
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

st.title("🏗️ 新規開発")

# メニューオプション
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🏗️ 開発室
    新規プロジェクトの企画・開発
    """)
    if st.button("開発室を開く", key="dev_room", use_container_width=True):
        st.switch_page("pages/development_room.py")

with col2:
    st.markdown("""
    ### 📊 プロジェクト管理室
    プロジェクトの進捗管理
    """)
    if st.button("プロジェクト管理室を開く", key="proj_mgmt", use_container_width=True):
        st.switch_page("pages/project_management.py")

with col3:
    st.markdown("""
    ### 🧪 A/Bテスト
    テストの作成と分析
    """)
    if st.button("A/Bテストを開く", key="ab_test", use_container_width=True):
        st.switch_page("pages/ab_testing.py")

st.markdown("---")

# その他のツール
st.subheader("その他の開発ツール")

col1, col2 = st.columns(2)

with col1:
    if st.button("📦 プロダクト管理", use_container_width=True):
        st.switch_page("pages/product_management.py")
        
with col2:
    if st.button("📋 ツール一覧", use_container_width=True):
        st.switch_page("pages/dev_tools_list.py")