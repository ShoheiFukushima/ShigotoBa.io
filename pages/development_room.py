#!/usr/bin/env python3
"""
開発室 - 新規プロジェクト開発・企画センター
Gemini Gemsとの連携とプロダクト情報入力
"""

import streamlit as st
import os
import sys
import json
import webbrowser
from datetime import datetime
import uuid

# ページ設定
st.set_page_config(
    page_title="開発室",
    page_icon="🏗️",
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
    
    /* パンくずナビゲーション */
    .breadcrumb {
        background: rgba(30, 41, 59, 0.5);
        padding: 10px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }
    
    .breadcrumb a {
        color: #3b82f6;
        text-decoration: none;
    }
    
    .breadcrumb a:hover {
        text-decoration: underline;
    }
    
    /* メインヘッダー */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* Geminiリンクカード */
    .gemini-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        border: 2px solid #3b82f6;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .gemini-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
    }
    
    .gemini-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .gemini-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #e2e8f0;
        margin-bottom: 10px;
    }
    
    .gemini-description {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 15px;
    }
    
    .gemini-button {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s;
        border: none;
        cursor: pointer;
    }
    
    .gemini-button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.5);
    }
    
    /* フォームセクション */
    .form-section {
        background: rgba(30, 41, 59, 0.5);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }
    
    .section-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
    
    /* プロンプト生成ボタン */
    .prompt-button {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.3s;
        margin-left: 10px;
    }
    
    .prompt-button:hover {
        background: rgba(16, 185, 129, 0.2);
        transform: translateY(-1px);
    }
    
    /* プロジェクトテンプレート */
    .template-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .template-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 20px;
        border-radius: 12px;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .template-card:hover {
        border-color: #3b82f6;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
    }
    
    .template-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .template-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #e2e8f0;
        margin-bottom: 10px;
    }
    
    .template-description {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* ステップインジケーター */
    .step-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 30px 0;
    }
    
    .step {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(59, 130, 246, 0.2);
        border: 2px solid rgba(59, 130, 246, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 10px;
        color: #94a3b8;
        font-weight: bold;
    }
    
    .step.active {
        background: #3b82f6;
        border-color: #3b82f6;
        color: white;
    }
    
    .step.completed {
        background: #10b981;
        border-color: #10b981;
        color: white;
    }
    
    .step-line {
        width: 50px;
        height: 2px;
        background: rgba(59, 130, 246, 0.3);
    }
    
    .step-line.completed {
        background: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'projects' not in st.session_state:
    st.session_state.projects = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'development_data' not in st.session_state:
    st.session_state.development_data = {}

# Gemini Gems URL定義
GEMINI_GEMS = {
    "content_generation": {
        "url": "https://gemini.google.com/gem/eba34d830526",
        "title": "コンテンツ生成Gem",
        "description": "マーケティングコンテンツの自動生成",
        "icon": "✨"
    },
    "tech_stack": {
        "url": "https://gemini.google.com/gem/15feb2aaf816", 
        "title": "技術スタック選定Gem",
        "description": "最適な技術選択をサポート",
        "icon": "🛠️"
    },
    "market_analysis": {
        "url": "https://gemini.google.com/gem/market_analysis",
        "title": "市場分析Gem",
        "description": "競合・市場の詳細分析",
        "icon": "📊"
    },
    "business_strategy": {
        "url": "https://gemini.google.com/gem/business_strategy",
        "title": "ビジネス戦略Gem", 
        "description": "事業戦略の策定支援",
        "icon": "🎯"
    }
}

# プロンプトテンプレート
PROMPT_TEMPLATE = """あなたはプロのAIプロンプトエンジニアです。

以下の情報を基に、最適化されたプロンプトを生成してください：

【プロダクト情報】
- 製品名: {product_name}
- カテゴリ: {category}
- ターゲット: {target}
- 独自価値: {unique_value}

【要求事項】
- 目的: {purpose}
- 出力形式: {output_format}
- 制約条件: {constraints}

【プロンプト要件】
1. 具体的で実行可能な指示
2. 期待する出力の明確な定義
3. 品質を保証する評価基準
4. 日本市場に最適化された内容

このプロンプトを使用して、{gem_type}での分析を実行してください。"""

def generate_prompt(product_data: dict, gem_type: str) -> str:
    """プロンプトを生成"""
    return PROMPT_TEMPLATE.format(
        product_name=product_data.get('name', 'N/A'),
        category=product_data.get('category', 'N/A'),
        target=product_data.get('target', 'N/A'),
        unique_value=product_data.get('unique_value', 'N/A'),
        purpose=f"{gem_type}の詳細分析",
        output_format="構造化されたデータと具体的な提案",
        constraints="日本市場向け、実用性重視",
        gem_type=gem_type
    )

# パンくずナビゲーション
st.markdown("""
<div class="breadcrumb">
    <a href="javascript:void(0)" onclick="window.parent.postMessage({type: 'streamlit:rerun', data: {page: 'home.py'}}, '*')">🏠 ダッシュボード</a>
    <span style="color: #94a3b8;"> > </span>
    <span style="color: #e2e8f0;">🏗️ 開発室</span>
</div>
""", unsafe_allow_html=True)

# メインヘッダー
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏗️ 開発室</h1>
    <p style="color: #94a3b8; font-size: 1.1rem;">新規プロダクトの企画・開発センター</p>
</div>
""", unsafe_allow_html=True)

# 戻るボタン
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("⬅️ ダッシュボードに戻る", type="secondary"):
        st.switch_page("app.py")

# ステップインジケーター
st.markdown("""
<div class="step-indicator">
    <div class="step completed">1</div>
    <div class="step-line completed"></div>
    <div class="step active">2</div>
    <div class="step-line"></div>
    <div class="step">3</div>
    <div class="step-line"></div>
    <div class="step">4</div>
</div>
""", unsafe_allow_html=True)

st.markdown("**Step 1:** アイデア発想 → **Step 2:** 詳細企画 → **Step 3:** 技術選定 → **Step 4:** 実装開始")

# タブ構成
tab1, tab2, tab3 = st.tabs(["🚀 新規プロジェクト", "🤖 AI支援ツール", "📋 プロジェクトテンプレート"])

with tab1:
    st.markdown("### 📝 プロダクト情報入力")
    
    with st.form("product_form"):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        st.markdown('<div class="section-title"><span class="section-icon">🎯</span>基本情報</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input(
                "プロダクト名",
                placeholder="例: TaskFlow AI",
                help="開発予定のプロダクト・サービス名"
            )
            
            category = st.selectbox(
                "カテゴリ",
                [
                    "Webアプリケーション",
                    "モバイルアプリ", 
                    "SaaS/クラウドサービス",
                    "AIツール",
                    "Eコマース",
                    "教育・学習",
                    "エンターテイメント",
                    "ビジネスツール",
                    "その他"
                ]
            )
            
            target_audience = st.text_area(
                "ターゲット層",
                placeholder="例: 中小企業の経営者・マネージャー層（30-50代）",
                help="想定するユーザー・顧客層"
            )
        
        with col2:
            price_model = st.selectbox(
                "価格モデル",
                [
                    "月額サブスクリプション",
                    "年額サブスクリプション", 
                    "買い切り",
                    "フリーミアム",
                    "従量課金",
                    "無料",
                    "その他"
                ]
            )
            
            estimated_price = st.text_input(
                "想定価格",
                placeholder="例: 月額980円〜",
                help="想定している価格帯"
            )
            
            unique_value = st.text_area(
                "独自価値・差別化要因",
                placeholder="例: AI による自動タスク優先度付けで従来ツールより30%効率向上",
                help="競合との違い、独自の強み"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><span class="section-icon">📋</span>詳細情報</div>', unsafe_allow_html=True)
        
        problem_statement = st.text_area(
            "解決したい課題",
            placeholder="例: 現在のタスク管理ツールは複雑で、優先順位設定が手動のため非効率",
            help="このプロダクトが解決する具体的な問題"
        )
        
        key_features = st.text_area(
            "主要機能（改行区切り）",
            placeholder="AIによるタスク自動優先順位付け\nスマート通知システム\nチーム連携機能\n進捗自動レポート",
            help="予定している主な機能を改行で区切って入力"
        )
        
        business_model = st.text_area(
            "ビジネスモデル",
            placeholder="例: SaaS型月額課金、企業向けライセンス販売、API提供",
            help="収益化の方法・戦略"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🚀 プロジェクトを作成", type="primary", use_container_width=True)
        
        if submitted and product_name:
            # 新規プロジェクトを作成
            project_id = str(uuid.uuid4())
            project_data = {
                'id': project_id,
                'name': product_name,
                'created_at': datetime.now().isoformat(),
                'flow_stage': 0,
                'status': 'active',
                'flow_data': {
                    'product': {
                        'name': product_name,
                        'category': category,
                        'target': target_audience,
                        'price_model': price_model,
                        'estimated_price': estimated_price,
                        'unique_value': unique_value,
                        'problem_statement': problem_statement,
                        'key_features': key_features.split('\n') if key_features else [],
                        'business_model': business_model
                    }
                }
            }
            
            st.session_state.projects[project_id] = project_data
            st.session_state.current_project_id = project_id
            
            st.success(f"✅ プロジェクト '{product_name}' を作成しました！")
            st.info("プロジェクト管理室で詳細を確認できます")
            
            # リダイレクトボタン
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 プロジェクト詳細を見る"):
                    st.switch_page("pages/project_detail.py")
            with col2:
                if st.button("📊 プロジェクト管理室へ"):
                    st.switch_page("pages/project_management.py")
        
        elif submitted:
            st.error("プロダクト名は必須です")

with tab2:
    st.markdown("### 🤖 AI支援ツール")
    st.caption("Gemini Gemsとの連携でプロダクト開発を加速")
    
    # プロダクト情報が入力されている場合、プロンプト生成機能を表示
    if 'current_project_id' in st.session_state and st.session_state.current_project_id:
        current_project = st.session_state.projects.get(st.session_state.current_project_id, {})
        product_data = current_project.get('flow_data', {}).get('product', {})
        
        if product_data:
            st.success(f"現在のプロジェクト: **{product_data.get('name', 'N/A')}**")
    
    # Gemini Gemsカード表示
    gems_col1, gems_col2 = st.columns(2)
    
    with gems_col1:
        for gem_key, gem_data in list(GEMINI_GEMS.items())[:2]:
            st.markdown(f"""
            <div class="gemini-card">
                <div class="gemini-icon">{gem_data['icon']}</div>
                <div class="gemini-title">{gem_data['title']}</div>
                <div class="gemini-description">{gem_data['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🚀 {gem_data['title']}を開く", key=f"open_{gem_key}"):
                    # 新しいタブでGeminiを開く
                    st.markdown(f'<script>window.open("{gem_data["url"]}", "_blank");</script>', unsafe_allow_html=True)
                    st.info(f"{gem_data['title']}を新しいタブで開きました")
            
            with col2:
                if st.button(f"📝 プロンプト生成", key=f"prompt_{gem_key}"):
                    if 'current_project_id' in st.session_state and st.session_state.current_project_id:
                        current_project = st.session_state.projects.get(st.session_state.current_project_id, {})
                        product_data = current_project.get('flow_data', {}).get('product', {})
                        
                        if product_data:
                            prompt = generate_prompt(product_data, gem_data['title'])
                            st.session_state[f"generated_prompt_{gem_key}"] = prompt
                            st.success("プロンプトを生成しました！")
                        else:
                            st.warning("プロダクト情報を先に入力してください")
                    else:
                        st.warning("プロジェクトを先に作成してください")
            
            # 生成されたプロンプトの表示
            if f"generated_prompt_{gem_key}" in st.session_state:
                with st.expander(f"生成されたプロンプト - {gem_data['title']}"):
                    st.text_area(
                        "プロンプト内容",
                        st.session_state[f"generated_prompt_{gem_key}"],
                        height=200,
                        key=f"prompt_display_{gem_key}"
                    )
                    
                    # コピーボタン
                    if st.button(f"📋 クリップボードにコピー", key=f"copy_{gem_key}"):
                        st.info("プロンプトをコピーしました（手動でコピーしてください）")
    
    with gems_col2:
        for gem_key, gem_data in list(GEMINI_GEMS.items())[2:]:
            st.markdown(f"""
            <div class="gemini-card">
                <div class="gemini-icon">{gem_data['icon']}</div>
                <div class="gemini-title">{gem_data['title']}</div>
                <div class="gemini-description">{gem_data['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🚀 {gem_data['title']}を開く", key=f"open_{gem_key}"):
                    st.markdown(f'<script>window.open("{gem_data["url"]}", "_blank");</script>', unsafe_allow_html=True)
                    st.info(f"{gem_data['title']}を新しいタブで開きました")
            
            with col2:
                if st.button(f"📝 プロンプト生成", key=f"prompt_{gem_key}"):
                    if 'current_project_id' in st.session_state and st.session_state.current_project_id:
                        current_project = st.session_state.projects.get(st.session_state.current_project_id, {})
                        product_data = current_project.get('flow_data', {}).get('product', {})
                        
                        if product_data:
                            prompt = generate_prompt(product_data, gem_data['title'])
                            st.session_state[f"generated_prompt_{gem_key}"] = prompt
                            st.success("プロンプトを生成しました！")
                        else:
                            st.warning("プロダクト情報を先に入力してください")
                    else:
                        st.warning("プロジェクトを先に作成してください")
            
            # 生成されたプロンプトの表示
            if f"generated_prompt_{gem_key}" in st.session_state:
                with st.expander(f"生成されたプロンプト - {gem_data['title']}"):
                    st.text_area(
                        "プロンプト内容",
                        st.session_state[f"generated_prompt_{gem_key}"],
                        height=200,
                        key=f"prompt_display_{gem_key}"
                    )
                    
                    if st.button(f"📋 クリップボードにコピー", key=f"copy_{gem_key}"):
                        st.info("プロンプトをコピーしました（手動でコピーしてください）")

with tab3:
    st.markdown("### 📋 プロジェクトテンプレート")
    st.caption("よくあるプロダクトタイプから選択して素早く開始")
    
    templates = [
        {
            "icon": "🤖",
            "title": "AIツール・サービス",
            "description": "機械学習やAIを活用したプロダクト。自動化、予測、分析ツールなど",
            "example": "ChatBot、画像認識、推薦システム"
        },
        {
            "icon": "💼",
            "title": "ビジネスSaaS",
            "description": "企業向けクラウドサービス。業務効率化、管理システムなど",
            "example": "CRM、プロジェクト管理、会計システム"
        },
        {
            "icon": "🛒",
            "title": "Eコマース・マーケットプレイス",
            "description": "オンライン販売プラットフォーム。商品・サービスの売買サイト",
            "example": "オンラインストア、マッチングサイト"
        },
        {
            "icon": "📱",
            "title": "モバイルアプリ",
            "description": "スマートフォン向けアプリケーション。ユーティリティ、ゲーム、SNSなど",
            "example": "生産性アプリ、フィットネス、ソーシャル"
        },
        {
            "icon": "🎓",
            "title": "教育・学習プラットフォーム",
            "description": "オンライン学習、スキルアップ、知識共有サービス",
            "example": "オンライン講座、スキル学習、資格対策"
        },
        {
            "icon": "🏥",
            "title": "ヘルスケア・ウェルネス",
            "description": "健康管理、医療支援、ウェルネス関連サービス",
            "example": "健康記録、テレヘルス、フィットネス"
        }
    ]
    
    st.markdown('<div class="template-grid">', unsafe_allow_html=True)
    
    template_cols = st.columns(2)
    
    for i, template in enumerate(templates):
        with template_cols[i % 2]:
            st.markdown(f"""
            <div class="template-card">
                <div class="template-icon">{template['icon']}</div>
                <div class="template-title">{template['title']}</div>
                <div class="template-description">{template['description']}</div>
                <div style="margin-top: 10px; font-size: 0.8rem; color: #6b7280;">
                    例: {template['example']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📝 {template['title']}で開始", key=f"template_{i}", use_container_width=True):
                # テンプレートに基づいて初期値を設定
                st.session_state.template_selected = template
                st.info(f"'{template['title']}' テンプレートを選択しました。上部の「新規プロジェクト」タブで詳細を入力してください。")
    
    st.markdown('</div>', unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("🏗️ 開発室ダッシュボード")
    
    # 現在のプロジェクト情報
    if 'current_project_id' in st.session_state and st.session_state.current_project_id:
        current_project = st.session_state.projects.get(st.session_state.current_project_id, {})
        if current_project:
            st.subheader("📂 現在のプロジェクト")
            st.success(f"**{current_project['name']}**")
            st.caption(f"作成日: {current_project['created_at'][:10]}")
            
            if st.button("📊 プロジェクト詳細", use_container_width=True):
                st.switch_page("pages/project_detail.py")
    else:
        st.info("プロジェクトが選択されていません")
    
    st.markdown("---")
    
    # 開発ステータス
    st.subheader("📈 開発統計")
    
    total_projects = len(st.session_state.projects)
    st.metric("総プロジェクト数", total_projects)
    
    active_projects = len([p for p in st.session_state.projects.values() if p.get('status') == 'active'])
    st.metric("アクティブプロジェクト", active_projects)
    
    # 最近の活動
    st.subheader("📅 最近の活動")
    
    if st.session_state.projects:
        recent_projects = sorted(
            st.session_state.projects.values(),
            key=lambda x: x.get('created_at', '2024-01-01'),
            reverse=True
        )[:3]
        
        for project in recent_projects:
            st.write(f"📋 {project['name']}")
            created_at = project.get('created_at', '不明')
            if created_at != '不明':
                st.caption(f"作成: {created_at[:10]}")
            else:
                st.caption("作成日: 不明")
    else:
        st.info("まだプロジェクトがありません")
    
    st.markdown("---")
    
    # クイックアクション
    st.subheader("⚡ クイックアクション")
    
    if st.button("📊 プロジェクト管理室", use_container_width=True):
        st.switch_page("pages/project_management.py")
    
    if st.button("🤖 AI設定", use_container_width=True):
        st.switch_page("pages/ai_settings.py")
    
    if st.button("💬 AIチャット", use_container_width=True):
        st.switch_page("pages/realtime_chat.py")
    
    st.markdown("---")
    
    # 外部リンク
    st.subheader("🔗 外部リンク")
    
    external_links = [
        {"name": "Gemini AI", "url": "https://gemini.google.com"},
        {"name": "GitHub", "url": "https://github.com"},
        {"name": "Figma", "url": "https://figma.com"},
        {"name": "Notion", "url": "https://notion.so"}
    ]
    
    for link in external_links:
        st.markdown(f"• [{link['name']}]({link['url']})")
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ダッシュボード", use_container_width=True):
        st.switch_page("app.py")

# フッター
st.markdown("---")
st.caption("💡 ヒント: Gemini Gemsを活用して効率的にプロダクト企画を進めましょう。生成されたプロンプトをコピーしてGeminiで実行してください。")