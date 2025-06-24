#!/usr/bin/env python3
"""
共通サイドバーコンポーネント
全ページで統一されたサイドバーを提供
"""

import streamlit as st
import sys
import os

# プロジェクトルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.project_context import initialize_projects, render_sidebar_project_info
except ImportError:
    # フォールバック: 直接定義
    def initialize_projects():
        if 'projects' not in st.session_state:
            st.session_state.projects = {
                "project_1": {"name": "ECサイトリニューアル", "type": "dev", "status": "進行中"},
                "project_2": {"name": "新製品キャンペーン", "type": "marketing", "status": "企画中"},
                "project_3": {"name": "ユーザー行動分析", "type": "analysis", "status": "分析中"},
                "project_4": {"name": "SaaSプラットフォーム開発", "type": "dev", "status": "開発中"},
                "project_5": {"name": "価格戦略最適化", "type": "analysis", "status": "検証中"}
            }
    
    def render_sidebar_project_info():
        if hasattr(st.session_state, 'current_project') and st.session_state.current_project:
            current_project_data = st.session_state.projects[st.session_state.current_project]
            st.markdown("### 📈 プロジェクト情報")
            if current_project_data['type'] == 'dev':
                st.info("🏗️ **推奨ツール**: 開発室、プロジェクト管理室、A/Bテスト")
            elif current_project_data['type'] == 'marketing':
                st.info("🎨 **推奨ツール**: AI Creative Studio、価格戦略、マルチプラットフォーム管理")
            elif current_project_data['type'] == 'analysis':
                st.info("📊 **推奨ツール**: パフォーマンスダッシュボード、アトリビューション分析")
            st.metric("プロジェクト進捗", "65%", "+15%")
            st.metric("今週のタスク", "8", "+3")
        else:
            st.markdown("### 📊 今週の統計")
            st.metric("完了タスク", "42", "+12")
            st.metric("生成コンテンツ", "156", "+34")
            st.metric("投稿数", "28", "+7")

def render_sidebar():
    """統一されたサイドバーをレンダリング"""
    with st.sidebar:
        # プロジェクト選択
        st.markdown("### 📁 プロジェクト選択")
        
        # プロジェクト一覧を初期化
        initialize_projects()
        
        # プロジェクト選択
        project_options = ["プロジェクトを選択..."] + [f"{pid}: {data['name']}" for pid, data in st.session_state.projects.items()]
        selected_project = st.selectbox(
            "現在のプロジェクト",
            project_options,
            key="selected_project"
        )
        
        # 選択されたプロジェクトの情報を保存
        if selected_project != "プロジェクトを選択...":
            project_id = selected_project.split(":")[0]
            st.session_state.current_project = project_id
            project_data = st.session_state.projects[project_id]
            
            # プロジェクト詳細表示
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                        padding: 15px; border-radius: 10px; margin: 10px 0;
                        border: 1px solid rgba(59, 130, 246, 0.2);">
                <p style="margin: 0; color: #3b82f6; font-weight: bold;">📊 {project_data['name']}</p>
                <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 0.9rem;">ステータス: {project_data['status']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.session_state.current_project = None
        
        st.markdown("---")
        
        # 1. 新規開発カテゴリ
        with st.expander("🏗️ 新規開発", expanded=False):
            if st.button("開発室", key="dev_room_nav", use_container_width=True):
                st.switch_page("pages/development_room.py")
            if st.button("プロジェクト管理室", key="project_mgmt_nav", use_container_width=True):
                st.switch_page("pages/project_management.py")
            if st.button("プロダクト管理", key="product_mgmt_nav", use_container_width=True):
                st.switch_page("pages/product_management.py")
            if st.button("A/Bテスト", key="ab_testing_nav", use_container_width=True):
                st.switch_page("pages/ab_testing.py")
            if st.button("新製品", key="new_product_nav", use_container_width=True):
                st.switch_page("pages/new_product.py")
            if st.button("プロジェクト詳細", key="project_detail_nav", use_container_width=True):
                st.switch_page("pages/project_detail.py")
            if st.button("ツール一覧", key="dev_tools_list_nav", use_container_width=True):
                st.switch_page("pages/dev_tools_list.py")
        
        # 2. 運営・分析カテゴリ
        with st.expander("📊 運営・分析", expanded=False):
            if st.button("パフォーマンスダッシュボード", key="performance_nav", use_container_width=True):
                st.switch_page("pages/performance_dashboard.py")
            if st.button("アトリビューション分析", key="attribution_nav", use_container_width=True):
                st.switch_page("pages/attribution_analysis.py")
            if st.button("カスタマージャーニー", key="customer_journey_nav", use_container_width=True):
                st.switch_page("pages/customer_journey_engine.py")
            if st.button("プロダクト分析", key="product_analysis_nav", use_container_width=True):
                st.switch_page("pages/product_analysis.py")
            if st.button("リアルタイムAIチャット", key="ai_chat_nav", use_container_width=True):
                st.switch_page("pages/realtime_chat.py")
            if st.button("AI設定", key="ai_settings_nav", use_container_width=True):
                st.switch_page("pages/ai_settings.py")
            if st.button("フローダッシュボード", key="flow_dashboard_nav", use_container_width=True):
                st.switch_page("pages/flow_dashboard.py")
            if st.button("ツール一覧", key="analysis_tools_list_nav", use_container_width=True):
                st.switch_page("pages/analysis_tools_list.py")
        
        # 3. 広告・マーケカテゴリ
        with st.expander("🎨 広告・マーケ", expanded=False):
            if st.button("AI Creative Studio", key="ai_creative_nav", use_container_width=True):
                st.switch_page("pages/ai_creative_studio.py")
            if st.button("リアルタイム広告最適化", key="realtime_ad_nav", use_container_width=True):
                st.switch_page("pages/realtime_ad_optimizer.py")
            if st.button("価格戦略コンサルティング", key="pricing_strategy_nav", use_container_width=True):
                st.switch_page("pages/pricing_strategy.py")
            if st.button("マルチプラットフォーム管理", key="multi_platform_nav", use_container_width=True):
                st.switch_page("pages/multi_platform_manager.py")
            if st.button("自動投稿", key="auto_posting_nav", use_container_width=True):
                st.switch_page("pages/auto_posting.py")
            if st.button("スケジューラー制御", key="scheduler_nav", use_container_width=True):
                st.switch_page("pages/scheduler_control.py")
            if st.button("ユーザーマニュアル", key="user_manual_nav", use_container_width=True):
                st.switch_page("pages/user_manual.py")
            if st.button("ツール一覧", key="marketing_tools_list_nav", use_container_width=True):
                st.switch_page("pages/marketing_tools_list.py")
        
        st.markdown("---")
        
        # プロジェクト関連情報表示
        render_sidebar_project_info()