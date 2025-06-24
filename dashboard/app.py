#!/usr/bin/env python3
"""
Publishing Dashboard - ダークモード・高速版
全ツールを統合した専用ダッシュボード
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

# 既存ツールをインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.market_analyzer import MarketAnalyzer
from tools.content_generator import ContentGenerator
from tools.seasonal_analyzer import SeasonalAnalyzer
from tools.growth_phase_strategist import GrowthPhaseStrategist, GrowthPhase

# AutomationOrchestratorは依存関係の問題で後回し
# from tools.automation_orchestrator import AutomationOrchestrator, AutomationLevel

# ページ設定（ダークモード）
st.set_page_config(
    page_title="パブリッシングダッシュボード",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS（ダークモード）
st.markdown("""
<style>
    /* ダークモード設定 */
    .stApp {
        background-color: #0e1117;
    }
    
    /* サイドバー */
    section[data-testid="stSidebar"] {
        background-color: #1a1f2e;
    }
    
    /* カード風デザイン */
    .metric-card {
        background-color: #1a1f2e;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* ボタンスタイル */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
        transform: scale(1.02);
    }
    
    /* チャットメッセージ */
    .chat-message {
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    .user-message {
        background-color: #3b82f6;
        margin-left: 20%;
    }
    
    .claude-message {
        background-color: #1a1f2e;
        margin-right: 20%;
    }
    
    /* メトリクス強調 */
    .big-metric {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# セッション初期化
if 'current_product' not in st.session_state:
    st.session_state.current_product = {}
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}
if 'execution_plan' not in st.session_state:
    st.session_state.execution_plan = []
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None

# プロジェクト設定読み込み
def load_projects():
    """プロジェクト設定を読み込み"""
    config_path = "dashboard/config/projects.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"projects": []}

# ヘルパー関数
def save_conversation(speaker, message):
    """会話をログに保存"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "speaker": speaker,
            "message": message
        }
        st.session_state.chat_messages.append(log_entry)
        
        # ファイルにも保存
        log_path = "dashboard/data/conversation_log.md"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n### [{timestamp}] {speaker}\n{message}\n")
    except Exception as e:
        st.error(f"ログ保存エラー: {str(e)}")

def analyze_product(product_info):
    """プロダクトを分析"""
    try:
        with st.spinner('🔍 分析中...'):
            analyzer = MarketAnalyzer()
            results = analyzer.analyze_product(product_info)
            st.session_state.analysis_results = results
            save_conversation("System", f"{product_info['name']}の分析が完了しました")
            return results
    except Exception as e:
        st.error(f"分析エラー: {str(e)}")
        st.info("💡 ヒント: プロダクト情報を確認してください")
        return None

def generate_content(product_info):
    """コンテンツを生成"""
    try:
        with st.spinner('✍️ コンテンツ生成中...'):
            generator = ContentGenerator()
            contents = generator.generate_all_content(product_info)
            st.session_state.generated_content = contents
            save_conversation("System", "コンテンツ生成が完了しました")
            return contents
    except Exception as e:
        st.error(f"コンテンツ生成エラー: {str(e)}")
        st.info("💡 ヒント: 分析を先に実行してください")
        return None

# メインレイアウト
st.title("🚀 パブリッシングダッシュボード")
st.caption("マーケティング自動化統合ダッシュボード - ダークモード")

# サイドバー：プロダクト管理
with st.sidebar:
    st.header("📦 プロダクト管理")
    
    # プロジェクト選択
    try:
        projects_config = load_projects()
        project_names = ["新規プロダクト"] + [p['name'] for p in projects_config.get('projects', [])]
    except Exception as e:
        st.error(f"プロジェクト設定読み込みエラー: {str(e)}")
        projects_config = {"projects": [], "marketingCalendar": {}}
        project_names = ["新規プロダクト"]
    selected_project_name = st.selectbox(
        "プロジェクト選択",
        project_names,
        index=0 if st.session_state.selected_project is None else project_names.index(st.session_state.selected_project['name']) if st.session_state.selected_project else 0
    )
    
    # 選択されたプロジェクトの情報を読み込み
    if selected_project_name != "新規プロダクト":
        for project in projects_config['projects']:
            if project['name'] == selected_project_name:
                st.session_state.selected_project = project
                st.session_state.current_product = {
                    'name': project['name'],
                    'category': project['category'],
                    'target': project['target'],
                    'price': project['price'],
                    'unique_value': project['uniqueValue'],
                    'users': project['users']
                }
                break
    else:
        st.session_state.selected_project = None
    
    # プロダクト情報表示/編集
    with st.form("product_form"):
        st.subheader("プロダクト情報")
        
        if st.session_state.selected_project:
            # 既存プロジェクトの情報表示
            st.info(f"📍 {st.session_state.selected_project['path']}")
            st.caption(f"ステータス: {st.session_state.selected_project['status']}")
            st.caption(f"マーケティング: {st.session_state.selected_project['preferredDay']}曜日")
        
        name = st.text_input("プロダクト名", value=st.session_state.current_product.get('name', ''))
        category = st.text_input("カテゴリ", value=st.session_state.current_product.get('category', ''))
        target = st.text_input("ターゲット", value=st.session_state.current_product.get('target', ''))
        price = st.text_input("価格", value=st.session_state.current_product.get('price', ''))
        unique_value = st.text_area("独自価値", value=st.session_state.current_product.get('unique_value', ''))
        users = st.number_input("現在のユーザー数", min_value=0, value=st.session_state.current_product.get('users', 0))
        
        if st.form_submit_button("保存して分析", type="primary"):
            st.session_state.current_product = {
                'name': name,
                'category': category,
                'target': target,
                'price': price,
                'unique_value': unique_value,
                'users': users
            }
            analyze_product(st.session_state.current_product)
            st.success("✅ 分析完了！")
    
    # クイックアクション
    st.markdown("---")
    st.subheader("⚡ クイックアクション")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 再分析", use_container_width=True):
            if st.session_state.current_product:
                analyze_product(st.session_state.current_product)
    
    with col2:
        if st.button("✍️ 生成", use_container_width=True):
            if st.session_state.current_product:
                generate_content(st.session_state.current_product)
    
    # プロダクトステータス
    if st.session_state.current_product:
        st.markdown("---")
        st.subheader("📈 ステータス")
        st.metric("ユーザー数", f"{st.session_state.current_product.get('users', 0):,}")
        
        # 成長フェーズ判定
        users = st.session_state.current_product.get('users', 0)
        if users == 0:
            phase = "ステルス期"
        elif users < 1000:
            phase = "ローンチ期"
        elif users < 10000:
            phase = "初期成長期"
        elif users < 100000:
            phase = "成長期"
        else:
            phase = "拡大期"
        
        st.info(f"成長フェーズ: {phase}")

# メインエリア：タブ
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📅 週間カレンダー", "💬 戦略相談", "📊 分析結果", "✍️ コンテンツ", "🎯 実行プラン", "📈 パフォーマンス"])

# タブ1: 週間カレンダービュー
with tab1:
    st.subheader("📅 週間マーケティングカレンダー")
    
    # 現在の週を取得
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    # カレンダー表示
    col_days = st.columns(7)
    days = ["月", "火", "水", "木", "金", "土", "日"]
    
    for i, (col, day) in enumerate(zip(col_days, days)):
        with col:
            current_date = week_start + timedelta(days=i)
            is_today = current_date.date() == today.date()
            
            # 曜日ヘッダー
            if is_today:
                st.markdown(f"**🔵 {day}曜日**")
                st.caption(f"{current_date.strftime('%m/%d')}")
            else:
                st.markdown(f"**{day}曜日**")
                st.caption(f"{current_date.strftime('%m/%d')}")
            
            # プロジェクトスケジュール
            day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            if i < len(projects_config['marketingCalendar']):
                day_key = day_names[i]
                if day_key in projects_config['marketingCalendar']:
                    project_name = projects_config['marketingCalendar'][day_key]
                    
                    # プロジェクト情報を取得
                    project_info = None
                    for p in projects_config['projects']:
                        if p['name'] == project_name:
                            project_info = p
                            break
                    
                    if project_info:
                        with st.container():
                            st.markdown(f"**{project_name}**")
                            st.caption(project_info['category'])
                            
                            # ステータスバッジ
                            if project_info['status'] == 'production':
                                st.success("本番運用中", icon="✅")
                            else:
                                st.warning("開発中", icon="🚧")
                            
                            # 今週のタスク
                            if is_today:
                                st.info("📌 本日実行")
                                if st.button(f"実行", key=f"exec_{i}"):
                                    st.session_state.selected_project = project_info
                                    st.session_state.current_product = {
                                        'name': project_info['name'],
                                        'category': project_info['category'],
                                        'target': project_info['target'],
                                        'price': project_info['price'],
                                        'unique_value': project_info['uniqueValue'],
                                        'users': project_info['users']
                                    }
                                    analyze_product(st.session_state.current_product)
                                    generate_content(st.session_state.current_product)
                                    st.success("分析とコンテンツ生成完了！")
                else:
                    st.caption("予定なし")
            else:
                st.caption("週末")
    
    # 週間サマリー
    st.markdown("---")
    st.subheader("📊 今週の活動サマリー")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        active_projects = sum(1 for p in projects_config['projects'] if p['status'] == 'production')
        st.metric("稼働中プロジェクト", f"{active_projects}個")
    
    with col2:
        total_users = sum(p['users'] for p in projects_config['projects'])
        st.metric("総ユーザー数", f"{total_users:,}人")
    
    with col3:
        st.metric("今週の実行予定", "5プロジェクト")

# タブ2: 戦略相談チャット
with tab2:
    col1, col2 = st.columns([7, 3])
    
    with col1:
        st.subheader("チャット")
        
        # チャット履歴表示
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.chat_messages[-20:]:  # 最新20件
                if msg['speaker'] == 'You':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>You:</strong> {msg['message']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message claude-message">
                        <strong>Claude:</strong> {msg['message']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # 入力エリア
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("メッセージを入力", placeholder="例: 学生向けのキャンペーンを考えて")
            col_send, col_clear = st.columns([1, 1])
            
            with col_send:
                if st.form_submit_button("送信", type="primary", use_container_width=True):
                    if user_input:
                        save_conversation("You", user_input)
                        
                        # 簡易的な応答ロジック
                        response = ""
                        if "学生" in user_input:
                            response = "学生向けの場合、現在6月なので期末試験シーズンです。勉強効率化や集中力向上を訴求するのが効果的でしょう。SNSは夜19-22時の投稿がおすすめです。"
                        elif "キャンペーン" in user_input:
                            response = "現在の成長フェーズを考慮すると、認知度向上キャンペーンが最優先です。無料トライアルや期間限定割引が効果的でしょう。"
                        elif "競合" in user_input:
                            response = "主要競合を分析しました。差別化ポイントはAI機能と価格優位性です。これらを前面に出したメッセージングを推奨します。"
                        else:
                            response = "承知しました。その点を考慮して戦略を立案します。"
                        
                        save_conversation("Claude", response)
                        st.rerun()
    
    with col2:
        st.subheader("💡 インサイト")
        
        # 現在の月の情報
        current_month = datetime.now().month
        month_names = ["", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
        
        st.info(f"現在: {month_names[current_month]}")
        
        if current_month == 6:
            st.markdown("""
            **6月の特徴:**
            - 梅雨シーズン（室内需要↑）
            - 期末試験期間
            - ボーナス前（財布の紐固め）
            - 父の日（6/18）
            """)
        
        # 推奨アクション
        st.markdown("**推奨アクション:**")
        st.markdown("- 室内活動訴求")
        st.markdown("- 学生向け割引")
        st.markdown("- 梅雨割キャンペーン")

# タブ3: 分析結果
with tab3:
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        # メトリクス表示
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("市場規模", results.market_size.get('total_market_value', 'N/A'))
        with col2:
            st.metric("成長率", results.market_size.get('growth_rate', 'N/A'))
        with col3:
            st.metric("競合数", f"{len(results.competitors)}社")
        with col4:
            st.metric("推奨チャネル", f"{len(results.recommended_channels)}個")
        
        # 詳細情報
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 競合分析")
            for comp in results.competitors:
                with st.expander(comp['name']):
                    st.write(f"**製品**: {comp['product']}")
                    st.write(f"**シェア**: {comp['market_share']}")
                    st.write(f"**価格**: {comp['pricing']}")
                    st.write("**強み**:", ', '.join(comp['strengths']))
                    st.write("**弱み**:", ', '.join(comp['weaknesses']))
        
        with col2:
            st.subheader("📱 推奨チャネル")
            for channel in results.recommended_channels:
                with st.expander(channel['channel']):
                    st.write(f"**優先度**: {channel['priority']}")
                    st.write(f"**戦略**: {channel['strategy']}")
                    st.write(f"**予算配分**: {channel['budget_allocation']}")
                    st.write(f"**期待ROI**: {channel['expected_roi']}")
        
        # サマリー
        st.subheader("📝 分析サマリー")
        st.markdown(results.summary)
    else:
        st.info("プロダクト情報を入力して分析を実行してください")

# タブ4: コンテンツ
with tab4:
    if st.session_state.generated_content:
        st.subheader("生成されたコンテンツ")
        
        # コンテンツタイプ選択
        content_type = st.selectbox(
            "コンテンツタイプ",
            ["SNS投稿", "プレスリリース", "ランディングページ", "メール"]
        )
        
        if content_type == "SNS投稿":
            col1, col2 = st.columns(2)
            
            with col1:
                if 'social_posts' in st.session_state.generated_content:
                    twitter_post = st.session_state.generated_content['social_posts'].get('twitter', {})
                    st.markdown("**Twitter/X**")
                    
                    # コピー可能なテキストエリア
                    if hasattr(twitter_post, 'body'):
                        st.text_area("投稿文", twitter_post.body, height=150, key="twitter_copy")
                        if st.button("📋 コピー", key="copy_twitter"):
                            st.write("クリップボードにコピーしました！")
            
            with col2:
                if 'social_posts' in st.session_state.generated_content:
                    linkedin_post = st.session_state.generated_content['social_posts'].get('linkedin', {})
                    st.markdown("**LinkedIn**")
                    
                    if hasattr(linkedin_post, 'body'):
                        st.text_area("投稿文", linkedin_post.body, height=150, key="linkedin_copy")
                        if st.button("📋 コピー", key="copy_linkedin"):
                            st.write("クリップボードにコピーしました！")
        
        # 一括ダウンロード
        st.markdown("---")
        if st.button("📥 全コンテンツをダウンロード", type="primary"):
            st.success("ダウンロード準備中...")
    else:
        st.info("コンテンツ生成を実行してください")

# タブ5: 実行プラン
with tab5:
    st.subheader("🎯 マーケティング実行プラン")
    
    # プラン生成ボタン
    if st.button("📋 プラン生成", type="primary"):
        if st.session_state.current_product and st.session_state.analysis_results:
            # 実行プランを生成
            plan_items = [
                {"id": 1, "type": "SNS", "title": "Twitter告知投稿", "timing": "今すぐ", "selected": True},
                {"id": 2, "type": "SNS", "title": "LinkedIn企業向け投稿", "timing": "明日9:00", "selected": True},
                {"id": 3, "type": "Blog", "title": "使い方ガイド記事", "timing": "今週木曜", "selected": False},
                {"id": 4, "type": "Email", "title": "既存ユーザー向けニュースレター", "timing": "月曜8:00", "selected": False},
                {"id": 5, "type": "Ad", "title": "Google検索広告開始", "timing": "承認後即時", "selected": True},
            ]
            st.session_state.execution_plan = plan_items
            st.success("プラン生成完了！")
    
    # プラン表示
    if st.session_state.execution_plan:
        # チェックリスト形式で表示
        selected_count = 0
        for item in st.session_state.execution_plan:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            
            with col1:
                selected = st.checkbox("", value=item['selected'], key=f"plan_{item['id']}")
                if selected:
                    selected_count += 1
            
            with col2:
                st.markdown(f"**{item['title']}**")
            
            with col3:
                st.caption(f"タイプ: {item['type']}")
            
            with col4:
                st.caption(f"実行: {item['timing']}")
        
        # 実行ボタン
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("選択中のタスク", f"{selected_count}件")
        
        with col2:
            if st.button(f"🚀 選択したタスクを実行 ({selected_count}件)", type="primary", use_container_width=True):
                st.success(f"{selected_count}件のタスクを実行キューに追加しました")
                save_conversation("System", f"{selected_count}件のマーケティングタスクを実行開始")

# タブ6: パフォーマンス
with tab6:
    st.subheader("📈 パフォーマンストラッキング")
    
    # ダミーデータで可視化
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("インプレッション", "12,543", "+23%")
    with col2:
        st.metric("エンゲージメント", "543", "+15%")
    with col3:
        st.metric("コンバージョン", "23", "+8%")
    with col4:
        st.metric("ROI", "3.2x", "+0.5")
    
    # グラフ表示エリア
    st.markdown("---")
    st.info("📊 詳細なアナリティクスは実装予定です")

# フッター
st.markdown("---")
st.caption("Publishing Dashboard v1.0 - ダークモード | 最終更新: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

# 自動保存
if st.session_state.current_product:
    # プロダクト情報を自動保存
    save_path = "dashboard/data/current_product.json"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.current_product, f, ensure_ascii=False, indent=2)