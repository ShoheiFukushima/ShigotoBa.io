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
    
    /* スケジュールアイテム */
    .schedule-item {
        background: rgba(30, 41, 59, 0.5);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 3px solid #10b981;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .schedule-time {
        color: #3b82f6;
        font-weight: bold;
        margin-right: 15px;
    }
    
    /* TODOアイテム */
    .todo-item {
        background: rgba(30, 41, 59, 0.5);
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        transition: all 0.2s;
    }
    
    .todo-item:hover {
        background: rgba(30, 41, 59, 0.8);
    }
    
    .todo-checkbox {
        margin-right: 10px;
    }
    
    .todo-priority-high {
        border-left: 3px solid #ef4444;
    }
    
    .todo-priority-medium {
        border-left: 3px solid #f59e0b;
    }
    
    .todo-priority-low {
        border-left: 3px solid #10b981;
    }
    
    /* メールアイテム */
    .email-item {
        background: rgba(30, 41, 59, 0.5);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .email-item:hover {
        background: rgba(30, 41, 59, 0.8);
    }
    
    .email-unread {
        border-left: 3px solid #3b82f6;
        font-weight: bold;
    }
    
    .email-subject {
        color: #e2e8f0;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    
    .email-sender {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* リンクカード */
    .link-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .link-card:hover {
        background: rgba(59, 130, 246, 0.2);
        transform: translateY(-5px);
    }
    
    .link-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .link-title {
        color: #e2e8f0;
        font-weight: bold;
    }
    
    /* ドキュメントアイテム */
    .doc-item {
        background: rgba(30, 41, 59, 0.5);
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .doc-item:hover {
        background: rgba(30, 41, 59, 0.8);
    }
    
    .doc-icon {
        margin-right: 10px;
    }
    
    /* ステータスバッジ */
    .status-badge {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
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

# メインコンテンツ - 1列レイアウト（TODOとプロジェクト状況のみ）
main_col1, main_col2 = st.columns([3, 2])

with main_col1:
    # 最近のアクティビティ
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
            priority_class = f"todo-priority-{todo['priority']}"
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

st.markdown("---")

# 開発リンク集
st.markdown("### 🚀 クイックアクセス")

# カテゴリ1: プロジェクト開発系
st.markdown("#### 🏗️ プロジェクト開発")
dev_links = [
    {"icon": "🏗️", "title": "開発室", "page": "development_room"},
    {"icon": "📊", "title": "プロジェクト\n管理室", "page": "project_management"},
    {"icon": "📦", "title": "プロダクト\n管理", "page": "product_management"},
    {"icon": "🧪", "title": "A/Bテスト", "page": "ab_testing"}
]

dev_cols = st.columns(4)
for idx, link in enumerate(dev_links):
    with dev_cols[idx]:
        if st.button(f"{link['icon']}\n\n{link['title']}", key=f"dev_{idx}", use_container_width=True):
            st.switch_page(f"pages/{link['page']}.py")

# カテゴリ2: プロジェクト運営系
st.markdown("#### 📈 プロジェクト運営・分析")
operation_links = [
    {"icon": "📈", "title": "パフォーマンス", "page": "performance_dashboard"},
    {"icon": "🎯", "title": "アトリビューション\n分析", "page": "attribution_analysis"},
    {"icon": "🛤️", "title": "カスタマー\nジャーニー", "page": "customer_journey_engine"},
    {"icon": "💬", "title": "AIチャット", "page": "realtime_chat"}
]

op_cols = st.columns(4)
for idx, link in enumerate(operation_links):
    with op_cols[idx]:
        if st.button(f"{link['icon']}\n\n{link['title']}", key=f"op_{idx}", use_container_width=True):
            st.switch_page(f"pages/{link['page']}.py")

# カテゴリ3: 広告・マーケティング実行系
st.markdown("#### 🎨 広告・マーケティング実行")
marketing_links = [
    {"icon": "🎨", "title": "AI Creative\nStudio", "page": "ai_creative_studio"},
    {"icon": "⚡", "title": "リアルタイム\n最適化", "page": "realtime_ad_optimizer"},
    {"icon": "🌐", "title": "マルチ\nプラットフォーム", "page": "multi_platform_manager"},
    {"icon": "📚", "title": "マニュアル", "page": "user_manual"},
    {"icon": "⚙️", "title": "設定", "page": "ai_settings"}
]

marketing_cols = st.columns(5)
for idx, link in enumerate(marketing_links):
    with marketing_cols[idx]:
        if st.button(f"{link['icon']}\n\n{link['title']}", key=f"marketing_{idx}", use_container_width=True):
            st.switch_page(f"pages/{link['page']}.py")

st.markdown("---")

# ドキュメント書庫
st.markdown("### 📚 ドキュメント書庫")

# ツリー表示用のスタイル追加
st.markdown("""
<style>
    .tree-container {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 2px solid rgba(59, 130, 246, 0.2);
    }
    
    .tree-category {
        margin-bottom: 20px;
    }
    
    .tree-category-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    
    .tree-category-icon {
        margin-right: 10px;
        font-size: 1.3rem;
    }
    
    .tree-item {
        margin-left: 30px;
        padding: 8px 15px;
        border-left: 2px solid rgba(59, 130, 246, 0.3);
        position: relative;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s;
    }
    
    .tree-item:hover {
        background: rgba(59, 130, 246, 0.1);
        border-left-color: #3b82f6;
    }
    
    .tree-item::before {
        content: '└─';
        position: absolute;
        left: -15px;
        color: rgba(59, 130, 246, 0.5);
    }
    
    .tree-item-name {
        display: flex;
        align-items: center;
        color: #e2e8f0;
    }
    
    .tree-item-icon {
        margin-right: 8px;
    }
    
    .tree-item-size {
        color: #94a3b8;
        font-size: 0.85rem;
    }
    
    .tree-subcategory {
        margin-left: 20px;
        margin-bottom: 15px;
    }
    
    .tree-subcategory-header {
        font-size: 1rem;
        color: #60a5fa;
        margin-bottom: 8px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

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
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📄</span>
                SNS運用マニュアル
            </span>
            <span class="tree-item-size">PDF・1.2MB</span>
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📄</span>
                KPI設定ガイドライン
            </span>
            <span class="tree-item-size">PDF・524KB</span>
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
            <span class="tree-item-size">XLSX・3.1MB</span>
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📄</span>
                競合分析まとめ_202501
            </span>
            <span class="tree-item-size">PDF・4.5MB</span>
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📈</span>
                市場調査データ
            </span>
            <span class="tree-item-size">CSV・892KB</span>
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📊</span>
                ROI分析シート
            </span>
            <span class="tree-item-size">XLSX・1.8MB</span>
        </div>
    </div>
    
    <!-- カテゴリ3: クリエイティブ素材 -->
    <div class="tree-category">
        <div class="tree-category-header">
            <span class="tree-category-icon">🎨</span>
            クリエイティブ素材
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📄</span>
                ブランドガイドライン
            </span>
            <span class="tree-item-size">PDF・8.2MB</span>
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">🎨</span>
                ロゴ素材集
            </span>
            <span class="tree-item-size">ZIP・15.3MB</span>
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">🎨</span>
                SNSテンプレート
            </span>
            <span class="tree-item-size">PSD・23.1MB</span>
        </div>
        <div class="tree-item">
            <span class="tree-item-name">
                <span class="tree-item-icon">📊</span>
                プレゼン資料雛形
            </span>
            <span class="tree-item-size">PPTX・5.4MB</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("⚡ クイックアクション")
    
    if st.button("➕ 新規プロジェクト", type="primary", use_container_width=True):
        st.switch_page("pages/development_room.py")
    
    if st.button("📝 新規TODO追加", use_container_width=True):
        st.info("TODO追加機能は開発中です")
    
    if st.button("📧 メール作成", use_container_width=True):
        st.info("メール作成機能は開発中です")
    
    st.markdown("---")
    
    st.header("📊 今週の統計")
    
    st.metric("完了タスク", "42", "+12")
    st.metric("生成コンテンツ", "156", "+34")
    st.metric("投稿数", "28", "+7")
    
    st.markdown("---")
    
    st.header("🔔 通知")
    
    notifications = [
        {"text": "新製品キャンペーンが承認されました", "time": "5分前"},
        {"text": "競合分析レポートが更新されました", "time": "1時間前"},
        {"text": "SNS投稿がスケジュールされました", "time": "3時間前"}
    ]
    
    for notif in notifications:
        st.info(f"**{notif['text']}**\n\n_{notif['time']}_")