#!/usr/bin/env python3
"""
プロジェクトコンテキスト管理ユーティリティ
全ページで選択されたプロジェクトのコンテキストを共有
"""

import streamlit as st

def initialize_projects():
    """プロジェクト一覧を初期化"""
    if 'projects' not in st.session_state:
        st.session_state.projects = {
            "project_1": {"name": "ECサイトリニューアル", "type": "dev", "status": "進行中"},
            "project_2": {"name": "新製品キャンペーン", "type": "marketing", "status": "企画中"},
            "project_3": {"name": "ユーザー行動分析", "type": "analysis", "status": "分析中"},
            "project_4": {"name": "SaaSプラットフォーム開発", "type": "dev", "status": "開発中"},
            "project_5": {"name": "価格戦略最適化", "type": "analysis", "status": "検証中"}
        }

def get_current_project():
    """現在選択されているプロジェクトを取得"""
    if hasattr(st.session_state, 'current_project') and st.session_state.current_project:
        return st.session_state.projects.get(st.session_state.current_project)
    return None

def get_current_project_id():
    """現在選択されているプロジェクトIDを取得"""
    if hasattr(st.session_state, 'current_project'):
        return st.session_state.current_project
    return None

def render_project_context():
    """プロジェクトコンテキストに応じた表示内容を返す"""
    current_project = get_current_project()
    
    if current_project:
        return f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                    padding: 15px; border-radius: 10px; margin: 10px 0;
                    border: 1px solid rgba(59, 130, 246, 0.2);">
            <p style="margin: 0; color: #3b82f6; font-weight: bold;">📊 {current_project['name']}</p>
            <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 0.9rem;">ステータス: {current_project['status']}</p>
        </div>
        """
    return ""

def get_project_specific_content(page_type):
    """プロジェクトタイプに応じた推奨コンテンツを取得"""
    current_project = get_current_project()
    
    if not current_project:
        return None
    
    project_type = current_project['type']
    project_name = current_project['name']
    
    # ページタイプとプロジェクトタイプの組み合わせによる推奨コンテンツ
    recommendations = {
        'dev': {
            'development_room': f"🎯 **{project_name}**の開発計画を策定しましょう",
            'project_management': f"📊 **{project_name}**の進捗管理とタスク分析",
            'product_management': f"📦 **{project_name}**の機能要件と改善計画",
            'ab_testing': f"🧪 **{project_name}**のA/Bテスト設計と検証",
            'performance_dashboard': f"📈 **{project_name}**の開発メトリクス監視",
        },
        'marketing': {
            'ai_creative_studio': f"🎨 **{project_name}**のクリエイティブ制作",
            'pricing_strategy': f"💰 **{project_name}**の価格戦略最適化",
            'multi_platform_manager': f"🌐 **{project_name}**のマルチチャネル配信",
            'performance_dashboard': f"📈 **{project_name}**のマーケティング効果測定",
            'attribution_analysis': f"🎯 **{project_name}**のROI分析",
        },
        'analysis': {
            'performance_dashboard': f"📊 **{project_name}**のKPI監視ダッシュボード",
            'attribution_analysis': f"🎯 **{project_name}**の成果要因分析",
            'customer_journey_engine': f"🛤️ **{project_name}**のユーザー行動分析",
            'product_analysis': f"📊 **{project_name}**のプロダクト利用分析",
            'realtime_chat': f"💬 **{project_name}**のデータについてAIに質問",
        }
    }
    
    return recommendations.get(project_type, {}).get(page_type)

def render_sidebar_project_info():
    """サイドバー用のプロジェクト情報表示"""
    current_project = get_current_project()
    
    if current_project:
        st.markdown("### 📈 プロジェクト情報")
        
        # プロジェクトタイプに応じた推奨ツール
        if current_project['type'] == 'dev':
            st.info("🏗️ **推奨ツール**: 開発室、プロジェクト管理室、A/Bテスト")
        elif current_project['type'] == 'marketing':
            st.info("🎨 **推奨ツール**: AI Creative Studio、価格戦略、マルチプラットフォーム管理")
        elif current_project['type'] == 'analysis':
            st.info("📊 **推奨ツール**: パフォーマンスダッシュボード、アトリビューション分析")
        
        # プロジェクトメトリクス
        st.metric("プロジェクト進捗", "65%", "+15%")
        st.metric("今週のタスク", "8", "+3")
    else:
        st.markdown("### 📊 今週の統計")
        st.metric("完了タスク", "42", "+12")
        st.metric("生成コンテンツ", "156", "+34")
        st.metric("投稿数", "28", "+7")