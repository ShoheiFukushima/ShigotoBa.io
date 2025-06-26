#!/usr/bin/env python3
"""
旧フローダッシュボード - プロジェクト管理室へリダイレクト
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="リダイレクト中...",
    page_icon="🔄",
    layout="wide"
)

# 自動的にプロジェクト管理室へリダイレクト
st.info("📊 プロジェクト管理室へ移動します...")
st.switch_page("pages/project_management.py")