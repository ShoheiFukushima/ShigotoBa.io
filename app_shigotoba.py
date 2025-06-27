#!/usr/bin/env python3
"""
Shigotoba.io - 個人開発者向け全自動マーケティング代理店システム
14個のAI専門家モジュールによる工場レーン型ビジネスプロセス自動化
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

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ページ設定
st.set_page_config(
    page_title="Shigotoba.io - AI専門家集団",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'project_data' not in st.session_state:
    st.session_state.project_data = {}
if 'ai_outputs' not in st.session_state:
    st.session_state.ai_outputs = {}
if 'approval_status' not in st.session_state:
    st.session_state.approval_status = {}
if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []

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

# ナビゲーション
def navigate_to(page: str):
    """ページ遷移"""
    st.session_state.current_page = page
    st.rerun()

# サイドバー
def render_sidebar():
    """サイドバーの表示"""
    with st.sidebar:
        st.title("🏭 Shigotoba.io")
        st.markdown("---")
        
        # ナビゲーションメニュー
        st.subheader("メニュー")
        if st.button("🏠 ホーム", use_container_width=True):
            navigate_to('home')
        if st.button("📝 企画書入力", use_container_width=True):
            navigate_to('planning')
        if st.button("🤖 AI実行状況", use_container_width=True):
            navigate_to('ai_status')
        if st.button("✅ 承認ゲート", use_container_width=True):
            navigate_to('approval')
        if st.button("📊 レポート", use_container_width=True):
            navigate_to('report')
        
        st.markdown("---")
        
        # プロジェクト状況
        if st.session_state.project_data:
            st.subheader("📋 現在のプロジェクト")
            project = st.session_state.project_data
            st.write(f"**アプリ名**: {project.get('app_name', '未設定')}")
            st.write(f"**カテゴリ**: {project.get('category', '未設定')}")
            
            # 進捗状況
            st.subheader("📈 進捗")
            phase = st.session_state.get('current_phase', Phase.PLANNING)
            progress = {
                Phase.PLANNING: 0.1,
                Phase.PHASE1: 0.3,
                Phase.APPROVAL1: 0.5,
                Phase.PHASE2: 0.7,
                Phase.APPROVAL2: 0.9,
                Phase.MONITORING: 1.0
            }
            st.progress(progress.get(phase, 0))
            st.caption(f"現在: {phase.value}")
        
        st.markdown("---")
        st.caption("© 2024 Shigotoba.io")

# ホームページ
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
        3. **人間承認** - 戦略の確認と承認
        4. **制作・配信** - 広告素材制作と配信
        5. **継続改善** - データ分析と最適化
        """)
        
        if st.session_state.project_data:
            if st.button("📈 現在のプロジェクトを確認", use_container_width=True):
                navigate_to('ai_status')
    
    # 最近の実行履歴
    if st.session_state.execution_history:
        st.markdown("---")
        st.subheader("📜 最近の実行履歴")
        for history in st.session_state.execution_history[-5:]:
            with st.expander(f"{history['timestamp']} - {history['action']}"):
                st.json(history['details'])

# 企画書入力ページ
def render_planning():
    """企画書入力フォーム"""
    st.title("📝 プロジェクト企画書入力")
    st.markdown("アプリのアイデアを入力してください。AIが市場分析から広告配信まで全て自動で実行します。")
    
    with st.form("project_plan_form"):
        # 基本情報
        st.subheader("🎯 基本情報")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            app_name = st.text_input("アプリ名", max_chars=30, help="30文字以内で入力")
        with col2:
            category = st.selectbox("カテゴリ", [
                "仕事効率化", "エンタメ", "SNS", "教育", 
                "健康", "金融", "旅行", "その他"
            ])
        with col3:
            platforms = st.multiselect("プラットフォーム", ["iOS", "Android", "Web"])
        
        # コンセプト
        st.subheader("💡 コンセプト")
        concept_oneline = st.text_area(
            "一言で説明（エレベーターピッチ）", 
            max_chars=140,
            help="30秒で説明できる内容を140文字以内で"
        )
        
        problems = []
        st.write("**解決する課題**（最大3つ）")
        for i in range(3):
            problem = st.text_input(f"課題{i+1}", key=f"problem_{i}")
            if problem:
                problems.append(problem)
        
        # ターゲット
        st.subheader("👥 ターゲット")
        target_users = st.text_area(
            "メインユーザー",
            help="年齢層/性別/職業/ライフスタイルなど"
        )
        usage_scenes = st.text_area(
            "利用シーン",
            help="いつ、どこで、どのように使うか"
        )
        
        # 機能
        st.subheader("⚡ 機能")
        st.write("**コア機能**（必須3つ）")
        core_features = []
        for i in range(3):
            feature = st.text_input(f"コア機能{i+1}", key=f"core_{i}")
            if feature:
                core_features.append(feature)
        
        st.write("**差別化機能**（1-2つ）")
        unique_features = []
        for i in range(2):
            feature = st.text_input(f"差別化機能{i+1}", key=f"unique_{i}")
            if feature:
                unique_features.append(feature)
        
        # 収益モデル
        st.subheader("💰 収益モデル")
        col1, col2 = st.columns(2)
        with col1:
            monetization = st.radio("課金方式", [
                "無料（広告）", "買い切り", "月額サブスク", 
                "年額サブスク", "フリーミアム"
            ])
        with col2:
            price_range = st.text_input("価格帯イメージ", placeholder="例: 基本無料、プレミアム月額500-1000円")
        
        # 追加情報（任意）
        with st.expander("📌 追加情報（任意）"):
            competitors = st.text_area("競合アプリ", placeholder="例: Todoist, Notion, Asana")
            budget = st.selectbox("開発予算", [
                "", "50万円以下", "50-200万円", "200-500万円", "500万円以上"
            ])
            release_date = st.date_input("希望リリース時期", value=None)
        
        # 送信ボタン
        submitted = st.form_submit_button("🚀 AI分析を開始", type="primary", use_container_width=True)
        
        if submitted:
            # バリデーション
            errors = []
            if not app_name:
                errors.append("アプリ名を入力してください")
            if not platforms:
                errors.append("プラットフォームを選択してください")
            if not concept_oneline:
                errors.append("コンセプトを入力してください")
            if len(problems) < 1:
                errors.append("解決する課題を最低1つ入力してください")
            if not target_users:
                errors.append("メインユーザーを入力してください")
            if not usage_scenes:
                errors.append("利用シーンを入力してください")
            if len(core_features) < 3:
                errors.append("コア機能を3つ入力してください")
            if not price_range:
                errors.append("価格帯イメージを入力してください")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # プロジェクトデータの保存
                project = ProjectPlan(
                    app_name=app_name,
                    category=category,
                    platforms=platforms,
                    concept_oneline=concept_oneline,
                    problems=problems,
                    target_users=target_users,
                    usage_scenes=usage_scenes,
                    core_features=core_features,
                    unique_features=unique_features,
                    monetization=monetization,
                    price_range=price_range,
                    competitors=competitors if competitors else None,
                    budget=budget if budget else None,
                    release_date=release_date.isoformat() if release_date else None
                )
                
                st.session_state.project_data = asdict(project)
                st.session_state.current_phase = Phase.PHASE1
                
                # 実行履歴に追加
                st.session_state.execution_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'action': 'プロジェクト作成',
                    'details': {'app_name': app_name, 'category': category}
                })
                
                st.success("✅ 企画書を受け付けました！AI分析を開始します...")
                st.balloons()
                
                # AI実行画面へ遷移
                navigate_to('ai_status')

# AI実行状況ページ
def render_ai_status():
    """AI実行状況の表示"""
    st.title("🤖 AI実行状況")
    
    if not st.session_state.project_data:
        st.warning("プロジェクトが設定されていません")
        if st.button("企画書入力へ"):
            navigate_to('planning')
        return
    
    # 現在のフェーズ表示
    phase = st.session_state.get('current_phase', Phase.PLANNING)
    st.info(f"現在のフェーズ: **{phase.value}**")
    
    # フェーズ1: 基礎戦略
    if phase.value in [Phase.PHASE1.value, Phase.APPROVAL1.value, Phase.PHASE2.value, Phase.APPROVAL2.value, Phase.MONITORING.value]:
        st.subheader("📊 フェーズ1: 基礎戦略")
        
        # AIモジュールの実行状況
        ai_modules_phase1 = [
            ("マーケット分析AI", "market_analysis", "📊"),
            ("グロースハッカーAI", "growth_hacker", "📈"),
            ("価格戦略AI", "pricing_strategy", "💰"),
            ("AI専門家会議システム", "ai_conference", "🤝"),
            ("コピーライティングAI", "copywriting", "✍️"),
            ("ビジュアルクリエイティブAI", "visual_creative", "🎨"),
            ("SEO/ASO専門AI", "seo_aso", "🔍")
        ]
        
        cols = st.columns(4)
        for idx, (name, key, icon) in enumerate(ai_modules_phase1):
            with cols[idx % 4]:
                status = st.session_state.ai_outputs.get(key, {}).get('status', 'pending')
                if status == 'completed':
                    st.success(f"{icon} {name}\n✅ 完了")
                elif status == 'running':
                    st.info(f"{icon} {name}\n🔄 実行中...")
                else:
                    st.warning(f"{icon} {name}\n⏳ 待機中")
        
        # AI実行ボタン
        if st.button("🚀 AI分析を実行", disabled=phase != Phase.PHASE1):
            asyncio.run(execute_phase1_ai())
    
    # 承認ゲート1の後のフェーズ
    if phase.value in [Phase.PHASE2.value, Phase.APPROVAL2.value, Phase.MONITORING.value]:
        st.markdown("---")
        st.subheader("🎬 フェーズ2: 実行戦略")
        
        ai_modules_phase2 = [
            ("修正反映AI", "revision_ai", "📝"),
            ("クリエイター実行AI", "creator_execution", "🎨"),
            ("広告配信AI", "ad_delivery", "📡"),
            ("データアナリストAI", "data_analyst", "📊"),
            ("カスタマーサクセスAI", "customer_success", "💬"),
            ("デプロイメントAI", "deployment", "🚀")
        ]
        
        cols = st.columns(3)
        for idx, (name, key, icon) in enumerate(ai_modules_phase2):
            with cols[idx % 3]:
                status = st.session_state.ai_outputs.get(key, {}).get('status', 'pending')
                if status == 'completed':
                    st.success(f"{icon} {name}\n✅ 完了")
                elif status == 'running':
                    st.info(f"{icon} {name}\n🔄 実行中...")
                else:
                    st.warning(f"{icon} {name}\n⏳ 待機中")
    
    # 詳細結果の表示
    if st.session_state.ai_outputs:
        st.markdown("---")
        st.subheader("📋 実行結果詳細")
        
        for key, output in st.session_state.ai_outputs.items():
            if output.get('status') == 'completed':
                with st.expander(f"{key} - 結果を見る"):
                    st.write(output.get('result', 'No result'))
                    st.caption(f"実行時刻: {output.get('timestamp', 'Unknown')}")

# 承認ゲートページ
def render_approval():
    """承認ゲートの表示"""
    st.title("✅ 承認ゲート")
    
    phase = st.session_state.get('current_phase', Phase.PLANNING)
    
    if phase == Phase.APPROVAL1:
        st.subheader("🚦 承認ゲート1: 基礎戦略の確認")
        
        # AI分析結果のサマリー表示
        st.info("AI専門家による分析が完了しました。以下の戦略を確認してください。")
        
        # タブで各結果を表示
        tabs = st.tabs(["📊 市場分析", "📈 成長戦略", "💰 価格戦略", "✍️ コピー", "🎨 ビジュアル", "🔍 SEO/ASO", "🤝 統合戦略"])
        
        with tabs[0]:
            st.write("**マーケット分析結果**")
            st.write(st.session_state.ai_outputs.get('market_analysis', {}).get('result', 'No data'))
        
        with tabs[1]:
            st.write("**グロース戦略**")
            st.write(st.session_state.ai_outputs.get('growth_hacker', {}).get('result', 'No data'))
        
        with tabs[2]:
            st.write("**価格戦略提案**")
            st.write(st.session_state.ai_outputs.get('pricing_strategy', {}).get('result', 'No data'))
        
        with tabs[3]:
            st.write("**コピーライティング成果物**")
            st.write(st.session_state.ai_outputs.get('copywriting', {}).get('result', 'No data'))
        
        with tabs[4]:
            st.write("**ビジュアル戦略**")
            st.write(st.session_state.ai_outputs.get('visual_creative', {}).get('result', 'No data'))
        
        with tabs[5]:
            st.write("**SEO/ASO最適化**")
            st.write(st.session_state.ai_outputs.get('seo_aso', {}).get('result', 'No data'))
        
        with tabs[6]:
            st.write("**AI専門家会議の統合戦略**")
            st.write(st.session_state.ai_outputs.get('ai_conference', {}).get('result', 'No data'))
        
        # 人文学者AIの解説（デモ）
        with st.expander("🎓 人文学者AIの解説"):
            st.write("""
            **文化的・社会的観点からの分析**
            
            このアプリは現代社会における「効率化への欲求」と「人間的なつながりの希求」の
            バランスを取ろうとする試みです。デジタル化が進む中で、人々は逆説的に
            より人間的な体験を求めており、このアプリはその需要に応えています。
            
            **注意点**: 過度な自動化は人間の創造性を奪う可能性があります。
            適切なバランスを保つことが重要です。
            """)
        
        # 修正指示入力
        st.markdown("---")
        revision_notes = st.text_area("修正指示（任意）", placeholder="修正が必要な箇所があれば入力してください")
        
        # 承認ボタン
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 承認して次へ", type="primary", use_container_width=True):
                st.session_state.approval_status['gate1'] = {
                    'approved': True,
                    'timestamp': datetime.now().isoformat(),
                    'revision_notes': revision_notes
                }
                st.session_state.current_phase = Phase.PHASE2
                
                # 修正指示があれば修正反映AIを実行
                if revision_notes:
                    st.session_state.ai_outputs['revision_ai'] = {
                        'status': 'completed',
                        'result': f"修正を反映しました: {revision_notes}",
                        'timestamp': datetime.now().isoformat()
                    }
                
                st.success("✅ 承認されました！フェーズ2を開始します。")
                navigate_to('ai_status')
        
        with col2:
            if st.button("🔄 修正を要求", use_container_width=True):
                st.warning("修正指示を入力してから承認してください。")
    
    elif phase == Phase.APPROVAL2:
        st.subheader("🚦 承認ゲート2: 制作物と配信計画の確認")
        
        # 制作物のプレビュー
        st.info("制作物と配信計画を確認してください。")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**制作された広告素材**")
            st.image("https://via.placeholder.com/300x250", caption="バナー広告（サンプル）")
        
        with col2:
            st.write("**配信計画**")
            st.write("""
            - **配信チャネル**: Google Ads, Facebook Ads
            - **予算配分**: 日額5,000円
            - **ターゲット**: 25-40歳、IT関連職
            - **配信期間**: 30日間
            """)
        
        # 承認ボタン
        if st.button("✅ 配信を開始", type="primary", use_container_width=True):
            st.session_state.approval_status['gate2'] = {
                'approved': True,
                'timestamp': datetime.now().isoformat()
            }
            st.session_state.current_phase = Phase.MONITORING
            st.success("✅ 広告配信を開始しました！")
            navigate_to('report')
    
    else:
        st.info("現在承認が必要な項目はありません。")
        if st.button("AI実行状況へ"):
            navigate_to('ai_status')

# レポートページ
def render_report():
    """レポート・分析結果の表示"""
    st.title("📊 レポート")
    
    if not st.session_state.project_data:
        st.warning("プロジェクトが設定されていません")
        return
    
    # プロジェクトサマリー
    st.subheader("📋 プロジェクトサマリー")
    project = st.session_state.project_data
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("アプリ名", project.get('app_name'))
        st.metric("カテゴリ", project.get('category'))
    with col2:
        st.metric("プラットフォーム", ", ".join(project.get('platforms', [])))
        st.metric("収益モデル", project.get('monetization'))
    with col3:
        st.metric("価格帯", project.get('price_range'))
        st.metric("作成日", project.get('created_at', '')[:10])
    
    # 実行結果サマリー
    st.markdown("---")
    st.subheader("🎯 実行結果サマリー")
    
    # フェーズ1の結果
    if Phase.APPROVAL1.value in [p.value for p in Phase] and st.session_state.ai_outputs:
        with st.expander("📊 フェーズ1: 基礎戦略"):
            for module, data in st.session_state.ai_outputs.items():
                if data.get('status') == 'completed':
                    st.write(f"**{module}**: ✅ 完了")
    
    # フェーズ2の結果
    if Phase.APPROVAL2.value in [p.value for p in Phase] and st.session_state.ai_outputs:
        with st.expander("🎬 フェーズ2: 実行戦略"):
            for module, data in st.session_state.ai_outputs.items():
                if module in ['revision_ai', 'creator_execution', 'ad_delivery']:
                    if data.get('status') == 'completed':
                        st.write(f"**{module}**: ✅ 完了")
    
    # パフォーマンスメトリクス（デモ）
    if st.session_state.get('current_phase') == Phase.MONITORING:
        st.markdown("---")
        st.subheader("📈 パフォーマンスメトリクス")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("インプレッション", "12,345", "+23%")
        with col2:
            st.metric("クリック率", "2.4%", "+0.3%")
        with col3:
            st.metric("コンバージョン", "123", "+15%")
        with col4:
            st.metric("CPA", "¥1,234", "-12%")
        
        st.info("📊 データアナリストAIが継続的に分析中...")
    
    # エクスポート機能
    st.markdown("---")
    if st.button("📥 レポートをダウンロード", use_container_width=True):
        # レポートデータの生成
        report_data = {
            'project': st.session_state.project_data,
            'ai_outputs': st.session_state.ai_outputs,
            'approval_status': st.session_state.approval_status,
            'execution_history': st.session_state.execution_history
        }
        
        # JSON形式でダウンロード
        st.download_button(
            label="JSONファイルをダウンロード",
            data=json.dumps(report_data, ensure_ascii=False, indent=2),
            file_name=f"shigotoba_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# AI実行関数
async def execute_phase1_ai():
    """フェーズ1のAI実行"""
    with st.spinner("AI専門家たちが分析中..."):
        progress_bar = st.progress(0)
        project_data = st.session_state.project_data
        
        try:
            # 1. マーケット分析AI
            progress_bar.progress(0.14)
            st.info("📊 マーケット分析AIが市場を調査中...")
            market_result = await shigotoba_modules.market_analysis_ai(project_data)
            st.session_state.ai_outputs['market_analysis'] = market_result
            
            if market_result['status'] == 'error':
                st.error(f"マーケット分析エラー: {market_result['error']}")
                return
            
            # 2. グロースハッカーAI（デモ）
            progress_bar.progress(0.28)
            st.info("📈 グロースハッカーAIが成長戦略を立案中...")
            await asyncio.sleep(1)  # デモ用
            growth_result = {
                'status': 'completed',
                'result': {
                    'acquisition_strategy': '初期はオーガニック中心、PMF後に広告展開',
                    'retention_plan': 'オンボーディング最適化とプッシュ通知戦略',
                    'viral_coefficient': 1.2,
                    'ltv_cac_ratio': 3.5
                }
            }
            st.session_state.ai_outputs['growth_hacker'] = growth_result
            
            # 3. 価格戦略AI（デモ）
            progress_bar.progress(0.42)
            st.info("💰 価格戦略AIが最適価格を算出中...")
            await asyncio.sleep(1)
            pricing_result = {
                'status': 'completed',
                'result': {
                    'recommended_price': '月額980円',
                    'freemium_features': ['基本タスク管理', '3プロジェクトまで'],
                    'premium_features': ['無制限プロジェクト', 'AI分析', 'チーム機能'],
                    'trial_period': '14日間'
                }
            }
            st.session_state.ai_outputs['pricing_strategy'] = pricing_result
            
            # 4. AI専門家会議システム
            progress_bar.progress(0.56)
            st.info("🤝 AI専門家会議で戦略を統合中...")
            conference_result = await shigotoba_modules.ai_conference_system(
                growth_result['result'],
                pricing_result['result'],
                market_result['result']
            )
            st.session_state.ai_outputs['ai_conference'] = conference_result
            
            # 5. コピーライティングAI
            progress_bar.progress(0.70)
            st.info("✍️ コピーライティングAIが魅力的な文章を作成中...")
            copy_result = await shigotoba_modules.copywriting_ai(
                project_data,
                market_result
            )
            st.session_state.ai_outputs['copywriting'] = copy_result
            
            # 6. ビジュアルクリエイティブAI（デモ）
            progress_bar.progress(0.84)
            st.info("🎨 ビジュアルクリエイティブAIがデザイン戦略を立案中...")
            await asyncio.sleep(1)
            visual_result = {
                'status': 'completed',
                'result': {
                    'color_palette': {
                        'primary': '#4A90E2',
                        'secondary': '#50C878',
                        'accent': '#F5A623'
                    },
                    'design_style': 'モダン・ミニマリスト',
                    'differentiators': '温かみのあるイラストとアニメーション'
                }
            }
            st.session_state.ai_outputs['visual_creative'] = visual_result
            
            # 7. SEO/ASO専門AI（デモ）
            progress_bar.progress(1.0)
            st.info("🔍 SEO/ASO専門AIが検索最適化中...")
            await asyncio.sleep(1)
            seo_result = {
                'status': 'completed',
                'result': {
                    'keywords': ['タスク管理', 'AI', 'スマート', '効率化', 'リモートワーク'],
                    'app_store_title': f"{project_data['app_name']} - AIタスク管理",
                    'meta_description': '最適化された説明文'
                }
            }
            st.session_state.ai_outputs['seo_aso'] = seo_result
            
            # フェーズ完了
            st.session_state.current_phase = Phase.APPROVAL1
            st.success("✅ フェーズ1の分析が完了しました！")
            st.balloons()
            
            # 実行履歴に追加
            st.session_state.execution_history.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'フェーズ1完了',
                'details': {
                    'total_cost': sum(
                        output.get('cost', 0) 
                        for output in st.session_state.ai_outputs.values() 
                        if isinstance(output, dict)
                    )
                }
            })
            
            # 承認ページへ自動遷移
            st.info("承認ゲートへ移動します...")
            await asyncio.sleep(2)
            navigate_to('approval')
            
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            logger.error(f"Phase 1 execution error: {e}")

# メイン処理
def main():
    """メインアプリケーション"""
    # サイドバー表示
    render_sidebar()
    
    # ページルーティング
    page = st.session_state.current_page
    
    if page == 'home':
        render_home()
    elif page == 'planning':
        render_planning()
    elif page == 'ai_status':
        render_ai_status()
    elif page == 'approval':
        render_approval()
    elif page == 'report':
        render_report()
    else:
        render_home()

if __name__ == "__main__":
    main()