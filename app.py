#!/usr/bin/env python3
"""
shigotoba.io - マーケティング自動化プラットフォーム
リファクタリング版 - 共通コンポーネントを使用
"""

import streamlit as st
from utils.page_config import setup_page
from utils.session_state import init_common_session_state
from utils.navigation import create_nav_buttons, get_nav_preset
from components.common_sidebar import render_sidebar, get_default_sidebar_config
from components.project_card import render_project_grid
from components.metrics import render_metrics_row
from components.onboarding import render_onboarding_modal, render_quick_start_guide, render_help_button
from components.favorites import render_favorites_section, render_recent_tools
from components.search import render_search_box, search_tools, render_search_results

# ページ設定（共通設定を使用）
setup_page("shigotoba.io - マーケティング自動化", "🚀", layout="wide")

# セッション状態の初期化（共通設定を使用）
init_common_session_state()

# Google Sheets接続状態を表示
try:
    from utils.google_sheets_db import get_db
    db = get_db()
    sheets_connected = db.spreadsheet is not None
    if sheets_connected:
        st.success("📊 Google Sheets データベース: 接続済み")
    else:
        st.warning("📊 Google Sheets データベース: 未接続 - [設定](/pages/_sheets_settings.py)で接続してください")
except:
    st.info("📊 Google Sheets データベース: 設定が必要 - [設定ページ](/pages/_sheets_settings.py)を確認してください")

# サイドバー設定をカスタマイズ
sidebar_config = get_default_sidebar_config()
sidebar_config['statistics'] = [
    {'label': 'タスク', 'value': '42', 'delta': '+12'},
    {'label': '投稿', 'value': '28', 'delta': '+7'},
    {'label': 'コンテンツ', 'value': '156', 'delta': '+34'},
    {'label': '効果', 'value': '89%', 'delta': '+5%'}
]

# サイドバーを表示
render_sidebar(sidebar_config)

# オンボーディングモーダル表示
render_onboarding_modal()

# ヘルプボタン表示
render_help_button()

# プロジェクト未選択時のウィザード表示
if st.session_state.get('show_project_wizard', False):
    from components.onboarding import render_project_setup_wizard
    render_project_setup_wizard()
else:
    # メインコンテンツ
    st.title("🏠 ダッシュボード")
    
    # 初心者向けクイックスタートガイド
    render_quick_start_guide()

# メトリクス表示
st.markdown("## 📊 今日の概要")
metrics_data = [
    {'label': 'アクティブプロジェクト', 'value': len(st.session_state.projects), 'delta': '+2'},
    {'label': '完了タスク', 'value': '42', 'delta': '+12'},
    {'label': '新規コンテンツ', 'value': '28', 'delta': '+7'},
    {'label': '効率スコア', 'value': '89%', 'delta': '+5%', 'delta_color': 'normal'}
]
render_metrics_row(metrics_data)

st.markdown("---")

# 検索機能とお気に入り
col1, col2 = st.columns([2, 1])

with col1:
    # ツール検索
    search_query = render_search_box()
    if search_query:
        results = search_tools(search_query)
        render_search_results(results, search_query)

with col2:
    # お気に入りセクション
    render_favorites_section()

# 最近使ったツール
render_recent_tools()

st.markdown("---")

# プロジェクト一覧
st.markdown("## 📋 プロジェクト一覧")
render_project_grid(st.session_state.projects, columns=3)

st.markdown("---")

# ツールへのクイックアクセス
st.markdown("## 🚀 クイックアクセス")

# カテゴリ1: 新規開発
st.markdown("### 🏗️ 新規開発")
create_nav_buttons(get_nav_preset('development'), columns=4)

# カテゴリ2: 運営・分析
st.markdown("### 📊 運営・分析")
create_nav_buttons(get_nav_preset('analytics'), columns=4)

# カテゴリ3: 広告・マーケティング
st.markdown("### 🎨 広告・マーケティング実行")
marketing_nav_items = get_nav_preset('marketing') + get_nav_preset('utilities')
create_nav_buttons(marketing_nav_items, columns=5)

# 新セクション: パイプライン
st.markdown("### 🔄 自動化パイプライン")
pipeline_items = [
    {'icon': '🔄', 'title': 'ワークフロー管理', 'page': 'pages/_workflow_manager.py', 'key': 'workflow'},
    {'icon': '📊', 'title': 'パイプラインモニター', 'page': 'pages/_pipeline_monitor.py', 'key': 'monitor'},
]
create_nav_buttons(pipeline_items, columns=4)