#!/usr/bin/env python3
"""
開発室 - リファクタリング版
統一されたスタイルとコンポーネントを使用
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import load_common_styles, render_page_header, render_metric_card, render_status_badge, render_progress_bar
from utils.page_config import setup_page
from utils.session_state import init_common_session_state
from components.common_sidebar import render_sidebar, get_default_sidebar_config

# ページ設定（共通設定を使用）
setup_page("開発室 - shigotoba.io", "📋", layout="wide")

# セッション状態の初期化
init_common_session_state()

# サイドバー設定
sidebar_config = get_default_sidebar_config()
sidebar_config['statistics'] = [
    {'label': 'タスク', 'value': '15', 'delta': '+3'},
    {'label': '完了', 'value': '8', 'delta': '+2'},
    {'label': '進捗', 'value': '53%', 'delta': '+8%'},
    {'label': '効率', 'value': '92%', 'delta': '+4%'}
]

# サイドバーを表示
render_sidebar(sidebar_config)

# 共通スタイル読み込み
load_common_styles()

# ページヘッダー
render_page_header(
    "開発室", 
    "プロジェクトの開発タスクを管理し、進捗を可視化します",
    "📋"
)

# 現在のプロジェクト情報（最適化）
current_project = None
if hasattr(st.session_state, 'current_project') and st.session_state.current_project:
    if hasattr(st.session_state, 'projects'):
        current_project = st.session_state.projects.get(st.session_state.current_project)

if current_project:
    st.markdown(f"""
    <div class="content-card" style="margin-bottom: 1rem;">
        <h3 style="color: #22c55e; margin: 0 0 0.5rem 0;">🏗️ 現在のプロジェクト</h3>
        <p style="color: #f1f5f9; margin: 0; font-size: 1.1rem;"><strong>{current_project['name']}</strong></p>
        <p style="color: #94a3b8; margin: 0.25rem 0 0 0;">ステータス: {render_status_badge(current_project['status'])}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ プロジェクトが選択されていません。サイドバーからプロジェクトを選択してください。")

# メインコンテンツ
tab1, tab2, tab3 = st.tabs(["📋 タスク管理", "📊 進捗状況", "🔧 ツール"])

with tab1:
    st.markdown("### 現在のタスク")
    
    # タスクの追加
    with st.expander("➕ 新しいタスクを追加"):
        task_name = st.text_input("タスク名")
        task_priority = st.select_slider("優先度", ["低", "中", "高"])
        if st.button("追加"):
            st.success(f"タスク '{task_name}' を追加しました！")
    
    # タスクリスト
    tasks = [
        {"name": "APIエンドポイントの実装", "priority": "高", "status": "進行中", "progress": 60},
        {"name": "データベース設計", "priority": "高", "status": "完了", "progress": 100},
        {"name": "フロントエンド統合", "priority": "中", "status": "未着手", "progress": 0},
        {"name": "テストケース作成", "priority": "中", "status": "進行中", "progress": 30}
    ]
    
    # タスクリスト表示（最適化）
    for i, task in enumerate(tasks):
        st.markdown(f"""
        <div class="content-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <h4 style="color: #f1f5f9; margin: 0; font-size: 1.1rem;">{task['name']}</h4>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                    {render_status_badge(task['status'])}
                    <span style="background-color: rgba(34, 197, 94, 0.2); color: #22c55e; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.8rem;">
                        {task['priority']}
                    </span>
                </div>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <span style="color: #94a3b8; font-size: 0.9rem;">進捗</span>
                    <span style="color: #22c55e; font-weight: 600;">{task['progress']}%</span>
                </div>
                {render_progress_bar(task['progress'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### プロジェクト進捗")
    
    # 全体進捗
    overall_progress = 47
    st.metric("全体進捗率", f"{overall_progress}%", "+5% (今週)")
    st.progress(overall_progress / 100)
    
    # フェーズ別進捗
    st.markdown("### フェーズ別進捗")
    phases = {
        "企画": 100,
        "設計": 100,
        "開発": 60,
        "テスト": 20,
        "デプロイ": 0
    }
    
    for phase, progress in phases.items():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"**{phase}**")
        with col2:
            st.progress(progress / 100)

with tab3:
    st.markdown("### 開発ツール")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔧 ユーティリティ")
        if st.button("🗂️ ファイル構造生成", use_container_width=True):
            st.code("""
project/
├── src/
│   ├── components/
│   ├── pages/
│   └── utils/
├── tests/
└── README.md
            """)
        
        if st.button("📝 README生成", use_container_width=True):
            st.info("プロジェクトのREADMEを自動生成します")
    
    with col2:
        st.markdown("#### 🧪 テスト")
        if st.button("✅ テスト実行", use_container_width=True):
            st.success("すべてのテストが成功しました！")
        
        if st.button("📊 カバレッジ確認", use_container_width=True):
            st.metric("テストカバレッジ", "87%", "+3%")

# フッター
st.markdown("---")
st.markdown("💡 **ヒント**: タスクをドラッグ&ドロップで並び替えることができます（実装予定）")