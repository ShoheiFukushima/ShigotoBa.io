#!/usr/bin/env python3
"""
開発室 - シンプル版
ヘッダーやサイドバーのインポートなし
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="開発室 - shigotoba.io",
    page_icon="📋",
    layout="wide"
)

# タイトル
st.title("📋 開発室")
st.markdown("プロジェクトの開発タスクを管理し、進捗を可視化します。")

# 現在のプロジェクト情報（セッション状態から取得）
if hasattr(st.session_state, 'current_project') and st.session_state.current_project:
    project = st.session_state.projects[st.session_state.current_project]
    st.info(f"🏗️ 現在のプロジェクト: **{project['name']}** ({project['status']})")
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
    
    for task in tasks:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
        with col1:
            st.markdown(f"**{task['name']}**")
        with col2:
            color = {"高": "🔴", "中": "🟡", "低": "🟢"}[task['priority']]
            st.markdown(f"{color} {task['priority']}")
        with col3:
            st.markdown(task['status'])
        with col4:
            st.progress(task['progress'] / 100)

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