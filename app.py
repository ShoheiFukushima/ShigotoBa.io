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

# ページ設定（共通設定を使用）
setup_page("shigotoba.io - マーケティング自動化", "🚀", layout="wide")

# セッション状態の初期化（共通設定を使用）
init_common_session_state()

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

# メインコンテンツ
st.title("🏠 ダッシュボード")

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