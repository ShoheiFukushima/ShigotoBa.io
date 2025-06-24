#!/usr/bin/env python3
"""
shigotoba.io - AI-Powered Marketing Automation Platform
Main entry point for Streamlit Cloud
"""

import streamlit as st
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="shigotoba.io - マーケティング自動化",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    /* ダークモード設定 */
    .stApp {
        background-color: #0e1117;
    }
    
    /* 固定ヘッダー */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 34px;
        background-color: #1a1f2e;
        border-bottom: 1px solid rgba(59, 130, 246, 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
        z-index: 10000;  /* 最上位レイヤー */
        max-width: 1080px;
        margin: 0 auto;
        width: 100%;
    }
    
    /* Streamlitのサイドバーのz-indexを調整 */
    section[data-testid="stSidebar"] {
        z-index: 9999;  /* ヘッダーの次のレイヤー */
        top: 34px !important;  /* ヘッダーの高さ分下げる */
        height: calc(100vh - 34px) !important;
    }
    
    /* サイドバーの内容もヘッダー分下げる */
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 10px;
    }
    
    .header-title {
        font-size: 11px;
        color: #e2e8f0;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .header-info {
        font-size: 11px;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    /* メインコンテンツのマージン調整 */
    .main {
        margin-top: 34px;
        position: relative;
        z-index: 1;  /* ベースレイヤー */
    }
    
    /* メインコンテンツエリアもヘッダー分調整 */
    .stMain {
        top: 34px !important;
        position: relative;
    }
    
    /* ウィジェットカード */
    .widget-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s;
    }
    
    .widget-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
    }
    
    .widget-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .widget-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #3b82f6;
    }
    
    /* グリーディングメッセージ */
    .greeting {
        font-size: 2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'todos' not in st.session_state:
    st.session_state.todos = [
        {"id": 1, "text": "マーケティングレポートの確認", "priority": "high", "done": False},
        {"id": 2, "text": "新製品のキャンペーン企画書作成", "priority": "high", "done": False},
        {"id": 3, "text": "SNS投稿スケジュールの更新", "priority": "medium", "done": False},
        {"id": 4, "text": "競合分析データの収集", "priority": "medium", "done": True},
        {"id": 5, "text": "チームミーティングの準備", "priority": "low", "done": False}
    ]

# 時間に応じた挨拶
current_hour = datetime.now().hour
if current_hour < 12:
    greeting = "おはようございます"
elif current_hour < 17:
    greeting = "こんにちは"
else:
    greeting = "こんばんは"

# ヘッダー
try:
    from components.header import render_header
    render_header()
except ImportError:
    # フォールバック
    st.markdown(f"""
    <div class="fixed-header">
        <span class="header-title">SHIGOTOBA.IO - マーケティング自動化プラットフォーム</span>
        <div class="header-info">
            <span>プロジェクト: {st.session_state.current_project if hasattr(st.session_state, 'current_project') and st.session_state.current_project else 'なし'}</span>
            <span>{datetime.now().strftime('%Y/%m/%d %H:%M')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="main">', unsafe_allow_html=True)

# ヘッダー
st.markdown(f'<h1 class="greeting">{greeting} 👋</h1>', unsafe_allow_html=True)
st.markdown(f"今日は {datetime.now().strftime('%Y年%m月%d日 %A')} です")

# 上部のメトリクス
col1, col2, col3, col4 = st.columns(4)

with col1:
    active_projects = len(st.session_state.get('projects', {}))
    st.metric("アクティブプロジェクト", active_projects, "+2")

with col2:
    pending_todos = len([t for t in st.session_state.todos if not t['done']])
    st.metric("未完了タスク", pending_todos, "-3")

with col3:
    st.metric("今週の成果", "24", "+8")

with col4:
    st.metric("効率スコア", "94%", "+5%")

st.markdown("---")

# メインコンテンツ
main_col1, main_col2 = st.columns([3, 2])

with main_col1:
    # システム活動概要
    st.markdown("""
    <div class="widget-card">
        <div class="widget-header">
            <span class="widget-title">📊 システム活動概要</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 20px;">
        <p>🚀 <strong>マーケティング自動化システム</strong>が正常に動作中</p>
        <p>🎯 <strong>AI機能</strong>: 広告最適化・コンテンツ生成・分析が利用可能</p>
        <p>📈 <strong>統合管理</strong>: 複数プラットフォームを一元管理</p>
        <p>🔧 <strong>カスタマイズ</strong>: あなたの業務に合わせて設定調整済み</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

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
            if st.checkbox(todo['text'], key=f"todo_{todo['id']}"):
                todo['done'] = True
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # プロジェクトステータス
    st.markdown("""
    <div class="widget-card">
        <div class="widget-header">
            <span class="widget-title">📊 プロジェクト状況</span>
        </div>
    """, unsafe_allow_html=True)
    
    if 'projects' in st.session_state and st.session_state.projects:
        for pid, project in list(st.session_state.projects.items())[:3]:
            progress = (project['flow_stage'] / 7) * 100
            st.write(f"**{project['name']}**")
            st.progress(progress / 100)
            st.caption(f"Stage {project['flow_stage'] + 1}/8 - {progress:.0f}%")
    else:
        st.info("プロジェクトがありません")
    
    st.markdown("</div>", unsafe_allow_html=True)

# サイドバー
try:
    from components.sidebar import render_sidebar
    render_sidebar()
except ImportError:
    # フォールバック: 元のサイドバー
    with st.sidebar:
        # プロジェクト選択
        st.markdown("### 📁 プロジェクト選択")
        
        # サンプルプロジェクト一覧
        if 'projects' not in st.session_state:
            st.session_state.projects = {
                "project_1": {"name": "ECサイトリニューアル", "type": "dev", "status": "進行中"},
                "project_2": {"name": "新製品キャンペーン", "type": "marketing", "status": "企画中"},
                "project_3": {"name": "ユーザー行動分析", "type": "analysis", "status": "分析中"},
                "project_4": {"name": "SaaSプラットフォーム開発", "type": "dev", "status": "開発中"},
                "project_5": {"name": "価格戦略最適化", "type": "analysis", "status": "検証中"}
            }
        
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
        
        # アコーディオンメニュー
        with st.expander("🏗️ 新規開発", expanded=False):
            if st.button("🏗️ 開発室", key="dev_room_nav", use_container_width=True):
                st.switch_page("pages/development_room.py")
            if st.button("📊 プロジェクト管理室", key="project_mgmt_nav", use_container_width=True):
                st.switch_page("pages/project_management.py")
            if st.button("📦 プロダクト管理", key="product_mgmt_nav", use_container_width=True):
                st.switch_page("pages/product_management.py")
            if st.button("🧪 A/Bテスト", key="ab_testing_nav", use_container_width=True):
                st.switch_page("pages/ab_testing.py")
            if st.button("📋 ツール一覧", key="dev_tools_list_nav", use_container_width=True):
                st.switch_page("pages/dev_tools_list.py")
        
        with st.expander("📊 運営・分析", expanded=False):
            if st.button("📈 パフォーマンスダッシュボード", key="performance_nav", use_container_width=True):
                st.switch_page("pages/performance_dashboard.py")
            if st.button("🎯 アトリビューション分析", key="attribution_nav", use_container_width=True):
                st.switch_page("pages/attribution_analysis.py")
            if st.button("🛤️ カスタマージャーニー", key="customer_journey_nav", use_container_width=True):
                st.switch_page("pages/customer_journey_engine.py")
            if st.button("📊 プロダクト分析", key="product_analysis_nav", use_container_width=True):
                st.switch_page("pages/product_analysis.py")
            if st.button("💬 リアルタイムAIチャット", key="ai_chat_nav", use_container_width=True):
                st.switch_page("pages/realtime_chat.py")
            if st.button("📋 ツール一覧", key="analysis_tools_list_nav", use_container_width=True):
                st.switch_page("pages/analysis_tools_list.py")
        
        with st.expander("🎨 広告・マーケ", expanded=False):
            if st.button("🎨 AI Creative Studio", key="ai_creative_nav", use_container_width=True):
                st.switch_page("pages/ai_creative_studio.py")
            if st.button("⚡ リアルタイム広告最適化", key="realtime_ad_nav", use_container_width=True):
                st.switch_page("pages/realtime_ad_optimizer.py")
            if st.button("💰 価格戦略コンサルティング", key="pricing_strategy_nav", use_container_width=True):
                st.switch_page("pages/pricing_strategy.py")
            if st.button("🌐 マルチプラットフォーム管理", key="multi_platform_nav", use_container_width=True):
                st.switch_page("pages/multi_platform_manager.py")
            if st.button("🚀 自動投稿", key="auto_posting_nav", use_container_width=True):
                st.switch_page("pages/auto_posting.py")
            if st.button("📋 ツール一覧", key="marketing_tools_list_nav", use_container_width=True):
                st.switch_page("pages/marketing_tools_list.py")
        
        st.markdown("---")
        
        # プロジェクト関連情報
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

# メインコンテンツdivを閉じる
try:
    from components.header import close_main_content
    close_main_content()
except ImportError:
    st.markdown('</div>', unsafe_allow_html=True)