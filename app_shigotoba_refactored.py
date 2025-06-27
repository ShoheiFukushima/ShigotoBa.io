#!/usr/bin/env python3
"""
Shigotoba.io - 個人開発者向け全自動マーケティング代理店システム
リファクタリング版 - 共通コンポーネントを使用
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from shigotoba_modules import shigotoba_modules
from utils.page_config import PagePresets
from utils.session_state import init_shigotoba_session_state
from utils.navigation import navigate_to
from components.common_sidebar import render_sidebar, get_shigotoba_sidebar_config
from components.metrics import render_progress_metric

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ページ設定（プリセットを使用）
PagePresets.shigotoba()

# セッション状態の初期化（専用設定を使用）
init_shigotoba_session_state()

# データクラス定義
@dataclass
class ProjectPlan:
    """企画書データクラス"""
    app_name: str
    category: str
    platforms: List[str]
    concept_oneline: str
    problems: List[str]
    target_users: str
    usage_scenes: str
    core_features: List[str]
    unique_features: List[str]
    monetization: str
    price_range: str
    competitors: Optional[str] = None
    budget: Optional[str] = None
    release_date: Optional[str] = None
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class Phase(Enum):
    """実行フェーズ"""
    PLANNING = "planning"
    PHASE1 = "phase1_strategy"
    APPROVAL1 = "approval1"
    PHASE2 = "phase2_execution"
    APPROVAL2 = "approval2"
    MONITORING = "monitoring"

# サイドバー設定
sidebar_config = get_shigotoba_sidebar_config()

# プロジェクトの進捗があれば表示
if st.session_state.project_data:
    current_phase = st.session_state.get('current_phase', Phase.PLANNING)
    progress_info = {
        Phase.PLANNING: {'name': '企画立案', 'progress': 10},
        Phase.PHASE1: {'name': '戦略策定', 'progress': 30},
        Phase.APPROVAL1: {'name': '第1承認', 'progress': 50},
        Phase.PHASE2: {'name': '実行準備', 'progress': 70},
        Phase.APPROVAL2: {'name': '第2承認', 'progress': 90},
        Phase.MONITORING: {'name': '監視運用', 'progress': 100}
    }
    
    # サイドバーにプロジェクト状況を追加
    sidebar_config['custom_sections'] = [
        {
            'title': '📋 現在のプロジェクト',
            'content': lambda: st.info(f"**{st.session_state.project_data.get('app_name', '未設定')}**\nカテゴリ: {st.session_state.project_data.get('category', '未設定')}"),
            'divider': True
        },
        {
            'title': '📈 進捗状況',
            'content': lambda: render_progress_metric(
                progress_info[current_phase]['name'],
                progress_info[current_phase]['progress'],
                100,
                unit="%",
                show_percentage=True
            ),
            'divider': False
        }
    ]

# サイドバーを表示
render_sidebar(sidebar_config)

# ページコンテンツの表示
current_page = st.session_state.current_page

if current_page == 'home':
    render_home()
elif current_page == 'planning':
    render_planning()
elif current_page == 'ai_status':
    render_ai_status()
elif current_page == 'approval':
    render_approval()
elif current_page == 'report':
    render_report()

def render_home():
    """ホームページの表示"""
    st.title("🏭 Shigotoba.io へようこそ")
    st.subheader("個人開発者向け全自動マーケティング代理店システム")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 特徴
        - **14個のAI専門家**が協力して作業
        - **企画から配信まで**全自動実行
        - **人間は承認するだけ**のシンプル設計
        - **工場レーン型**の明確なプロセス
        """)
        
        if st.button("🚀 新規プロジェクトを開始", type="primary", use_container_width=True):
            navigate_to('planning')
    
    with col2:
        st.markdown("""
        ### 📊 実行フロー
        1. **企画書入力** - アプリのアイデアを入力
        2. **AI分析** - 市場分析・戦略立案
        3. **承認ゲート** - 人間による確認・承認
        4. **自動実行** - マーケティング施策の実行
        5. **モニタリング** - 結果の監視・改善
        """)
    
    # 実行履歴
    if st.session_state.execution_history:
        st.markdown("---")
        st.markdown("### 📈 最近の実行履歴")
        for item in st.session_state.execution_history[-3:]:  # 最新3件
            st.markdown(f"- {item}")

def render_planning():
    """企画書入力ページ"""
    st.title("📝 企画書入力")
    st.markdown("あなたのアプリアイデアを入力してください。AI専門家チームが分析・戦略立案を行います。")
    
    with st.form("project_plan_form"):
        st.markdown("### 基本情報")
        col1, col2 = st.columns(2)
        
        with col1:
            app_name = st.text_input("アプリ名", help="作成したいアプリの名前")
            category = st.selectbox("カテゴリ", [
                "ビジネス・生産性", "ライフスタイル", "エンターテイメント", 
                "教育", "ヘルスケア", "ソーシャル", "ゲーム", "その他"
            ])
            platforms = st.multiselect("対象プラットフォーム", [
                "iOS", "Android", "Web", "デスクトップ"
            ])
        
        with col2:
            concept_oneline = st.text_area("ワンライン概要", 
                                         help="アプリの概要を1-2文で説明")
            monetization = st.selectbox("収益化方法", [
                "無料（広告収入）", "有料アプリ", "サブスクリプション", 
                "フリーミアム", "アプリ内課金", "その他"
            ])
            price_range = st.selectbox("価格帯", [
                "無料", "¥100-500", "¥500-1000", "¥1000-3000", 
                "¥3000以上", "月額¥500-1000", "月額¥1000以上"
            ])
        
        st.markdown("### 詳細情報")
        problems = st.text_area("解決したい課題", 
                               help="このアプリが解決する問題や課題を記述")
        target_users = st.text_area("ターゲットユーザー", 
                                   help="主要なユーザー層の特徴")
        usage_scenes = st.text_area("利用シーン", 
                                   help="ユーザーがどのような場面で使用するか")
        
        core_features = st.text_area("核となる機能", 
                                    help="アプリの中心となる機能（1行1機能）")
        unique_features = st.text_area("独自機能・差別化ポイント", 
                                     help="競合との差別化要素")
        
        submitted = st.form_submit_button("🚀 AI分析開始", type="primary")
        
        if submitted and app_name and concept_oneline:
            # データを保存
            project_plan = ProjectPlan(
                app_name=app_name,
                category=category,
                platforms=platforms,
                concept_oneline=concept_oneline,
                problems=problems.split('\n') if problems else [],
                target_users=target_users,
                usage_scenes=usage_scenes,
                core_features=core_features.split('\n') if core_features else [],
                unique_features=unique_features.split('\n') if unique_features else [],
                monetization=monetization,
                price_range=price_range
            )
            
            st.session_state.project_data = asdict(project_plan)
            st.session_state.current_phase = Phase.PHASE1
            
            st.success("✅ 企画書が保存されました！AI分析を開始します...")
            st.balloons()
            
            # AI分析状況ページに遷移
            navigate_to('ai_status')

def render_ai_status():
    """AI実行状況ページ"""
    st.title("🤖 AI実行状況")
    
    if not st.session_state.project_data:
        st.warning("先に企画書を入力してください。")
        if st.button("📝 企画書入力に戻る"):
            navigate_to('planning')
        return
    
    st.markdown(f"**プロジェクト**: {st.session_state.project_data['app_name']}")
    
    # AI モジュールの実行状況
    st.markdown("### 🏭 AI専門家の作業状況")
    
    modules = [
        {"name": "競合リスト生成", "status": "completed", "expert": "マーケットリサーチャー"},
        {"name": "コピーライティング", "status": "in_progress", "expert": "コピーライター"},
        {"name": "人文学者の視点", "status": "pending", "expert": "文化人類学者"},
        {"name": "AI専門家会議", "status": "pending", "expert": "AI戦略チーム"},
        {"name": "修正反映", "status": "pending", "expert": "プロジェクトマネージャー"}
    ]
    
    for module in modules:
        status_icon = {
            "completed": "✅",
            "in_progress": "🔄", 
            "pending": "⏳"
        }[module["status"]]
        
        status_color = {
            "completed": "#10b981",
            "in_progress": "#f59e0b",
            "pending": "#64748b"
        }[module["status"]]
        
        st.markdown(f"""
        <div class="ai-module-card" style="border-color: {status_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: {status_color};">{status_icon} {module['name']}</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #94a3b8;">担当: {module['expert']}</p>
                </div>
                <div style="color: {status_color}; font-weight: bold;">
                    {module['status'].upper()}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 手動で次のステップに進むボタン
    if st.button("📋 承認ゲートに進む", type="primary"):
        navigate_to('approval')

def render_approval():
    """承認ゲートページ"""
    st.title("✅ 承認ゲート")
    
    if not st.session_state.project_data:
        st.warning("先に企画書を入力してください。")
        return
    
    st.markdown("AI専門家チームからの提案をレビューして承認してください。")
    
    # 仮の提案内容
    st.markdown("### 📊 マーケティング戦略提案")
    
    tabs = st.tabs(["競合分析", "コピー案", "文化的考察", "AI戦略", "実行計画"])
    
    with tabs[0]:
        st.markdown("#### 競合分析結果")
        st.markdown("- 主要競合: 類似アプリA, アプリB, アプリC")
        st.markdown("- 市場ギャップ: 機能Xの不足")
        st.markdown("- 差別化ポイント: 独自機能Yで優位性")
    
    with tabs[1]:
        st.markdown("#### コピーライティング案")
        st.markdown("**キャッチコピー**: 「革新的な○○で、あなたの△△を変える」")
        st.markdown("**説明文**: ...")
    
    with tabs[2]:
        st.markdown("#### 文化人類学的考察")
        st.markdown("現代社会における○○の意味と、ユーザーの潜在的ニーズについて...")
    
    with tabs[3]:
        st.markdown("#### AI戦略提案")
        st.markdown("機械学習による○○機能の実装提案...")
    
    with tabs[4]:
        st.markdown("#### 実行計画")
        st.markdown("1. フェーズ1: ...")
        st.markdown("2. フェーズ2: ...")
    
    # 承認ボタン
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("❌ 却下", use_container_width=True):
            st.error("提案が却下されました。AI チームに再検討を依頼します。")
    
    with col2:
        if st.button("⚠️ 修正要求", use_container_width=True):
            st.warning("修正要求が送信されました。")
    
    with col3:
        if st.button("✅ 承認", type="primary", use_container_width=True):
            st.success("承認されました！実行フェーズに移行します。")
            st.balloons()
            st.session_state.current_phase = Phase.MONITORING

def render_report():
    """レポートページ"""
    st.title("📊 実行レポート")
    
    if not st.session_state.project_data:
        st.warning("まだ実行されたプロジェクトがありません。")
        return
    
    # 実行結果のサマリー
    st.markdown("### 📈 実行サマリー")
    
    metrics_data = [
        {'label': '広告表示回数', 'value': '12,450', 'delta': '+24%'},
        {'label': 'クリック率', 'value': '3.2%', 'delta': '+0.8%'},
        {'label': 'コンバージョン', 'value': '156', 'delta': '+45%'},
        {'label': 'ROI', 'value': '240%', 'delta': '+60%'}
    ]
    
    from components.metrics import render_metrics_row
    render_metrics_row(metrics_data)
    
    # 詳細分析
    st.markdown("### 📋 詳細分析")
    st.markdown("- **ターゲティング精度**: 高精度でターゲットユーザーにリーチ")
    st.markdown("- **クリエイティブ効果**: AIが生成したコピーが好評")
    st.markdown("- **改善提案**: さらなる最適化の余地あり")

# メイン実行部分の修正
if __name__ == "__main__":
    # 現在のページに基づいてコンテンツを表示
    current_page = st.session_state.current_page
    
    if current_page == 'home':
        render_home()
    elif current_page == 'planning':
        render_planning()
    elif current_page == 'ai_status':
        render_ai_status()
    elif current_page == 'approval':
        render_approval()
    elif current_page == 'report':
        render_report()
    else:
        # デフォルトはホーム
        render_home()