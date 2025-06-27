#!/usr/bin/env python3
"""
ダッシュボードホーム画面
リファクタリング版 - 共通コンポーネントを使用
"""

import streamlit as st
import sys
import os
from datetime import datetime

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.page_config import PagePresets
from utils.session_state import init_common_session_state, get_default_todos
from utils.navigation import create_nav_buttons, get_nav_preset
from components.common_sidebar import render_sidebar
from components.project_card import render_project_summary_cards
from components.metrics import render_metrics_row

# ページ設定（プリセットを使用）
PagePresets.dashboard()

# セッション状態の初期化
init_common_session_state()

# TODOリストの初期化
if 'todos' not in st.session_state:
    st.session_state.todos = get_default_todos()

# 時間に応じた挨拶
current_hour = datetime.now().hour
if current_hour < 12:
    greeting = "おはようございます"
elif current_hour < 17:
    greeting = "こんにちは"
else:
    greeting = "こんばんは"

# サイドバー設定
sidebar_config = {
    'branding': {
        'icon': '🏠',
        'title': 'SHIGOTOBA.IO',
        'subtitle': 'マーケティング自動化プラットフォーム',
        'show_date': True
    },
    'navigation': [
        {'icon': '🏠', 'label': 'ホーム', 'page': 'dashboard/home.py', 'key': 'home'},
        {'icon': '📋', 'label': '開発室', 'page': 'pages/_development_room.py', 'key': 'dev_room'},
        {'icon': '📊', 'label': 'プロジェクト管理', 'page': 'pages/_project_management.py', 'key': 'proj_mgmt'},
        {'icon': '📈', 'label': 'パフォーマンス', 'page': 'pages/_performance_dashboard.py', 'key': 'performance', 'divider_after': True},
        {'icon': '⚙️', 'label': '設定', 'page': 'pages/_ai_settings.py', 'key': 'settings'}
    ],
    'project_selector': {'show': True},
    'quick_actions': [
        {'icon': '➕', 'label': '新規プロジェクト', 'type': 'primary', 'key': 'new_project', 'callback': lambda: st.switch_page('pages/_project_management.py')},
        {'icon': '📝', 'label': 'タスク追加', 'type': 'secondary', 'key': 'new_task', 'callback': lambda: st.info('タスク追加機能は準備中です')}
    ],
    'statistics': [
        {'label': '完了タスク', 'value': len([t for t in st.session_state.todos if t['done']]), 'delta': '+3'},
        {'label': '投稿数', 'value': '28', 'delta': '+7'},
        {'label': 'コンテンツ', 'value': '156', 'delta': '+34'},
        {'label': '効率', 'value': '89%', 'delta': '+5%'}
    ],
    'notifications': [
        {'type': 'info', 'message': 'システムが正常に動作中', 'timestamp': datetime.now()},
        {'type': 'success', 'message': 'バックアップ完了', 'timestamp': datetime.now()},
    ],
    'show_footer': True
}

# サイドバーを表示
render_sidebar(sidebar_config)

# メインコンテンツ
st.markdown(f'<h1 class="greeting">{greeting} 👋</h1>', unsafe_allow_html=True)
st.markdown(f"今日は {datetime.now().strftime('%Y年%m月%d日 %A')} です")

# 上部のメトリクス
active_projects = len(st.session_state.get('projects', {}))
pending_todos = len([t for t in st.session_state.todos if not t['done']])

metrics_data = [
    {'label': 'アクティブプロジェクト', 'value': active_projects, 'delta': '+2'},
    {'label': '未完了タスク', 'value': pending_todos, 'delta': '-3'},
    {'label': '今週の成果', 'value': '24', 'delta': '+8'},
    {'label': '効率スコア', 'value': '94%', 'delta': '+5%'}
]
render_metrics_row(metrics_data)

st.markdown("---")

# メインコンテンツ - 2列レイアウト
main_col1, main_col2 = st.columns([3, 2])

with main_col1:
    # システム活動概要
    st.markdown("""
    <div class="widget-card">
        <div class="widget-header">
            <span class="widget-title">📊 システム活動概要</span>
        </div>
        <div style="padding: 20px;">
            <p>🚀 <strong>マーケティング自動化システム</strong>が正常に動作中</p>
            <p>🎯 <strong>AI機能</strong>: 広告最適化・コンテンツ生成・分析が利用可能</p>
            <p>📈 <strong>統合管理</strong>: 複数プラットフォームを一元管理</p>
            <p>🔧 <strong>カスタマイズ</strong>: あなたの業務に合わせて設定調整済み</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with main_col2:
    # TODOリスト
    st.markdown("""
    <div class="widget-card">
        <div class="widget-header">
            <span class="widget-title">✅ TODO</span>
        </div>
    """, unsafe_allow_html=True)
    
    for todo in st.session_state.todos:
        if not todo['done']:
            priority_class = f"todo-priority-{todo['priority']}"
            if st.checkbox(todo['text'], key=f"todo_{todo['id']}"):
                todo['done'] = True
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# プロジェクト状況
if st.session_state.get('projects'):
    st.markdown("## 📊 プロジェクト概要")
    render_project_summary_cards(st.session_state.projects)

st.markdown("---")

# クイックアクセス
st.markdown("## 🚀 クイックアクセス")

# カテゴリ1: プロジェクト開発
st.markdown("#### 🏗️ プロジェクト開発")
create_nav_buttons(get_nav_preset('development'), columns=4)

# カテゴリ2: プロジェクト運営・分析
st.markdown("#### 📈 プロジェクト運営・分析")
create_nav_buttons(get_nav_preset('analytics'), columns=4)

# カテゴリ3: 広告・マーケティング実行
st.markdown("#### 🎨 広告・マーケティング実行")
marketing_nav_items = get_nav_preset('marketing') + get_nav_preset('utilities')
create_nav_buttons(marketing_nav_items, columns=5)

st.markdown("---")

# ドキュメント書庫
st.markdown("### 📚 ドキュメント書庫")

# ツリー構造でドキュメントを表示
st.markdown("""
<div class="tree-container">
    <!-- カテゴリ1: マニュアル・ガイド -->
    <div class="tree-category">
        <div class="tree-category-header">
            <span class="tree-category-icon">📋</span>
            マニュアル・ガイド
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📄</span>
                システム利用ガイド
            </span>
            <span class="tree-item-size">PDF・2.3MB</span>
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📄</span>
                マーケティング戦略テンプレート
            </span>
            <span class="tree-item-size">DOCX・856KB</span>
        </div>
    </div>
    
    <!-- カテゴリ2: レポート・分析 -->
    <div class="tree-category">
        <div class="tree-category-header">
            <span class="tree-category-icon">📊</span>
            レポート・分析
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📊</span>
                2024年Q4実績レポート
            </span>
            <span class="tree-item-size">PDF・1.8MB</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)