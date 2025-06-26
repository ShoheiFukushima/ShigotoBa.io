#!/usr/bin/env python3
"""
shigotoba.io - マーケティング自動化プラットフォーム
シンプルで堅牢な構造、Streamlitの標準機能を最大限活用
リファクタリング済み - 2024年版
"""

import streamlit as st
from datetime import datetime

# ページ設定（これが最初に来る必要がある）
st.set_page_config(
    page_title="shigotoba.io",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'current_project' not in st.session_state:
    st.session_state.current_project = None

if 'projects' not in st.session_state:
    st.session_state.projects = {
        "project_1": {"name": "ECサイトリニューアル", "type": "dev", "status": "進行中"},
        "project_2": {"name": "新製品キャンペーン", "type": "marketing", "status": "企画中"},
        "project_3": {"name": "ユーザー行動分析", "type": "analysis", "status": "分析中"},
        "project_4": {"name": "SaaSプラットフォーム開発", "type": "dev", "status": "開発中"},
        "project_5": {"name": "価格戦略最適化", "type": "analysis", "status": "検証中"}
    }

# 共通CSS設定（最適化済み）
st.markdown("""
<style>
    /* グローバルスタイル */
    .stApp {
        background-color: #0e1117;
    }
    
    /* サイドバー最適化 */
    section[data-testid="stSidebar"] {
        background-color: #1e2329;
        border-right: 1px solid #2a3441;
    }
    
    section[data-testid="stSidebar"] button {
        width: 100%;
        text-align: left;
        margin-bottom: 0.25rem;
        background-color: transparent;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    
    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(34, 197, 94, 0.1);
        border-color: rgba(34, 197, 94, 0.3);
    }
    
    /* プロジェクトカード最適化 */
    .project-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(34, 197, 94, 0.2);
        transition: all 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(34, 197, 94, 0.15);
        border-color: rgba(34, 197, 94, 0.4);
    }
    
    /* メトリクス最適化 */
    .metric-container {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# サイドバー（Streamlit標準機能を活用）
with st.sidebar:
    # ブランディング（最適化）
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid #2a3441; margin-bottom: 1rem;">
        <h2 style="color: #22c55e; margin: 0; font-size: 1.5rem;">🚀 SHIGOTOBA.IO</h2>
        <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-style: italic;">マーケティング自動化プラットフォーム</p>
        <p style="color: #64748b; margin: 0.25rem 0 0 0; font-size: 0.8rem;">📅 {}</p>
    </div>
    """.format(datetime.now().strftime('%Y/%m/%d')), unsafe_allow_html=True)
    
    st.markdown("## 📁 プロジェクト")
    
    # プロジェクト選択
    project_names = ["選択してください"] + [data['name'] for data in st.session_state.projects.values()]
    selected = st.selectbox("現在の作業", project_names, label_visibility="collapsed")
    
    if selected != "選択してください":
        for pid, data in st.session_state.projects.items():
            if data['name'] == selected:
                st.session_state.current_project = pid
                st.info(f"📊 **{data['name']}**\nステータス: {data['status']}")
                break
    
    st.markdown("---")
    
    # ナビゲーション（Streamlitのページ機能を説明）
    st.markdown("## 🧭 ツール")
    st.markdown("""
    👈 左のページリストから選択するか、以下のクイックアクセスをご利用ください。
    
    ### 🏗️ 新規開発
    - 開発室
    - プロジェクト管理
    - A/Bテスト
    
    ### 📊 運営・分析  
    - パフォーマンス
    - アトリビューション
    - リアルタイムチャット
    
    ### 🎨 広告・マーケ
    - AI Creative Studio
    - 広告最適化
    - 価格戦略
    """)
    
    st.markdown("---")
    
    # 統計情報
    st.markdown("### 📈 今週の成果")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("タスク", "42", "+12")
        st.metric("投稿", "28", "+7")
    with col2:
        st.metric("コンテンツ", "156", "+34")
        st.metric("効果", "89%", "+5%")

# メインコンテンツ
st.title("🏠 ダッシュボード")

# プロジェクト一覧
st.markdown("## 📋 プロジェクト一覧")

cols = st.columns(3)
for i, (pid, project) in enumerate(st.session_state.projects.items()):
    with cols[i % 3]:
        # プロジェクトカード
        if project['type'] == 'dev':
            icon = "🏗️"
            color = "#3b82f6"
        elif project['type'] == 'marketing':
            icon = "🎨" 
            color = "#8b5cf6"
        else:
            icon = "📊"
            color = "#10b981"
            
        st.markdown(f"""
        <div class="project-card" style="border-color: {color}40;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <h3 style="color: {color}; margin: 0; font-size: 1.2rem;">{icon} {project['name']}</h3>
                <span style="background-color: {color}20; color: {color}; 
                      padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                    {project['type'].upper()}
                </span>
            </div>
            <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">📊 ステータス: <span style="color: {color};">{project['status']}</span></p>
            <div style="margin-top: 0.75rem; height: 2px; background: linear-gradient(90deg, {color}40 0%, transparent 100%);"></div>
        </div>
        """, unsafe_allow_html=True)

# ツールへのクイックアクセス
st.markdown("## 🚀 クイックアクセス")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏗️ 新規開発")
    if st.button("📋 開発室", use_container_width=True):
        st.switch_page("pages/_development_room.py")
    if st.button("📊 プロジェクト管理", use_container_width=True):
        st.switch_page("pages/_project_management.py")
    if st.button("🔄 A/Bテスト", use_container_width=True):
        st.switch_page("pages/_ab_testing.py")

with col2:
    st.markdown("### 📊 運営・分析")
    if st.button("📈 パフォーマンス", use_container_width=True):
        st.switch_page("pages/_performance_dashboard.py")
    if st.button("🔍 アトリビューション", use_container_width=True):
        st.switch_page("pages/_attribution_analysis.py")
    if st.button("💬 チャット", use_container_width=True):
        st.switch_page("pages/_realtime_chat.py")

with col3:
    st.markdown("### 🎨 広告・マーケ")
    if st.button("🎨 AI Creative", use_container_width=True):
        st.switch_page("pages/_ai_creative_studio.py")
    if st.button("🎯 広告最適化", use_container_width=True):
        st.switch_page("pages/_realtime_ad_optimizer.py")
    if st.button("💰 価格戦略", use_container_width=True):
        st.switch_page("pages/_pricing_strategy.py")