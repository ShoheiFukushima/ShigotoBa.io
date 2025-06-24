#!/usr/bin/env python3
"""
新規プロダクト開発ページ
Gemini Gemsとの連携とプロダクト情報入力
"""

import streamlit as st
import os
import sys
from datetime import datetime
import json
import webbrowser

# ページ設定
st.set_page_config(
    page_title="新規プロダクト開発",
    page_icon="🚀",
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
    
    /* メインヘッダー */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
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
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        transition: all 0.3s;
    }
    
    .gemini-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
    }
    
    .gemini-button {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        color: white;
        padding: 15px 40px;
        border-radius: 30px;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s;
    }
    
    .gemini-button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.5);
    }
    
    /* フォームセクション */
    .form-section {
        background: rgba(30, 41, 59, 0.5);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }
    
    .section-icon {
        font-size: 1.8rem;
        margin-right: 10px;
    }
    
    /* ステップインジケーター */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin-bottom: 40px;
        position: relative;
    }
    
    .step-indicator::before {
        content: "";
        position: absolute;
        top: 20px;
        left: 0;
        right: 0;
        height: 2px;
        background: #374151;
        z-index: 0;
    }
    
    .step {
        background: #374151;
        color: #94a3b8;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        position: relative;
        z-index: 1;
        transition: all 0.3s;
    }
    
    .step.active {
        background: #3b82f6;
        color: white;
        transform: scale(1.2);
    }
    
    .step.completed {
        background: #10b981;
        color: white;
    }
    
    /* ヒントボックス */
    .hint-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .hint-title {
        color: #3b82f6;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    /* プロンプトボタン */
    .prompt-button {
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid #3b82f6;
        color: #3b82f6;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s;
        margin-right: 10px;
    }
    
    .prompt-button:hover {
        background: rgba(59, 130, 246, 0.3);
        transform: scale(1.05);
    }
    
    .gemini-mini-button {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        border: none;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .gemini-mini-button:hover {
        transform: scale(1.05);
        box-shadow: 0 3px 10px rgba(59, 130, 246, 0.4);
    }
    
    /* テンプレートカード */
    .template-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        cursor: pointer;
        transition: all 0.3s;
        border: 1px solid transparent;
    }
    
    .template-card:hover {
        border-color: #3b82f6;
        transform: translateX(5px);
    }
    
    .template-card.selected {
        border-color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'new_product_step' not in st.session_state:
    st.session_state.new_product_step = 1
if 'product_draft' not in st.session_state:
    st.session_state.product_draft = {}
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = {}

# Gemini Gems リンク設定（実際のGem URL）
GEMINI_GEMS_LINKS = {
    "product_structure": "https://gemini.google.com/gem/19df7f90f8e1",  # 新規プロダクト情報の構造化
    "market_analysis": "https://gemini.google.com/gem/b89b496ba5e8",   # 市場分析Gem
    "competitor_analysis": "https://gemini.google.com/gem/83f977349707", # 競合分析Gem
    "benefit_extraction": "https://gemini.google.com/gem/adf821690025", # ベネフィット抽出Gem
    "content_generation": "https://gemini.google.com/gem/eba34d830526", # コンテンツ生成Gem
    "tech_stack": "https://gemini.google.com/gem/15feb2aaf816"         # 技術スタック選定Gem
}

# プロンプト生成関数
def generate_prompt(prompt_type, context=None):
    """各フィールド用のプロンプトを生成"""
    prompts = {
        "product_idea": f"""新製品のアイデアを以下の形式で整理してください：

【基本情報】
製品名: （覚えやすく、ブランド化しやすい名前）
カテゴリ: {context.get('category', '[選択したカテゴリ]')}
ターゲット: （具体的なペルソナ、年齢層、職業など）

【解決する課題】
（ユーザーが抱える具体的な問題を1-2文で）

【独自の価値提案】
1. （競合にない強み1）
2. （競合にない強み2）
3. （競合にない強み3）

【想定利用シーン】
（いつ、どこで、どのように使われるか）""",
        
        "market_analysis": f"""「{context.get('product_name', '[製品名]')}」の市場分析を以下の形式で出力してください：

【市場規模】
国内市場: ○○億円（2024年）
年間成長率: ○○%
グローバル市場: ○○億円

【主要競合】（上位3-5社）
1. 企業名（シェア○%）- 月額○○円〜
2. 企業名（シェア○%）- 月額○○円〜
3. 企業名（シェア○%）- 月額○○円〜

【市場トレンド】
- トレンド1: （具体的な動向）
- トレンド2: （具体的な動向）
- トレンド3: （具体的な動向）

【参入機会と脅威】
機会: （なぜ今参入すべきか）
脅威: （注意すべきリスク）""",
        
        "target_persona": f"""「{context.get('product_name', '[製品名]')}」のターゲットペルソナを詳細に定義してください：

【基本属性】
年齢: ○○〜○○歳
性別: 
職業: 
年収: ○○万円〜○○万円
居住地: 

【行動特性】
- デジタルリテラシー: [高/中/低]
- 購買決定要因: 
- 情報収集方法: 
- 利用デバイス: 

【課題とニーズ】
現在の課題:
1. 
2. 
3. 

期待する解決策:
1. 
2. 
3. 

【購買行動】
- 予算感: 月額○○円まで
- 決裁権: [あり/なし/影響力あり]
- 導入障壁: """,
        
        "mvp_features": f"""「{context.get('product_name', '[製品名]')}」のMVP機能を優先順位付けして提案してください：

【必須機能（Must Have）】
1. 機能名: 説明（なぜ必須か）
2. 機能名: 説明（なぜ必須か）
3. 機能名: 説明（なぜ必須か）

【あると良い機能（Nice to Have）】
1. 機能名: 説明（付加価値）
2. 機能名: 説明（付加価値）
3. 機能名: 説明（付加価値）

【将来の拡張機能（Future）】
1. 機能名: 説明（Phase 2以降）
2. 機能名: 説明（Phase 2以降）
3. 機能名: 説明（Phase 2以降）

【技術的考慮事項】
- 開発期間の見積もり
- 必要なリソース
- 技術的な課題""",
        
        "pricing_strategy": f"""「{context.get('product_name', '[製品名]')}」の価格戦略を提案してください：

【価格プラン構成】
無料プラン:
- 機能制限: 
- ユーザー数: 
- 目的: （なぜ無料プランを提供するか）

スタータープラン: 月額¥○○
- 含まれる機能: 
- ユーザー数: 
- サポート: 

プロプラン: 月額¥○○
- 含まれる機能: 
- ユーザー数: 
- サポート: 

エンタープライズ: 要見積もり
- カスタマイズ可能な機能
- SLA保証
- 専任サポート

【価格設定の根拠】
- 競合比較での位置づけ
- 提供価値との整合性
- ターゲットの支払い意欲

【収益予測】
- 無料→有料転換率: ○○%
- 平均顧客単価: ¥○○
- LTV: ¥○○"""
    }
    
    return prompts.get(prompt_type, "プロンプトが見つかりません")

def open_gemini_with_prompt(prompt_text):
    """Geminiを新しいタブで開く（プロンプト付き）"""
    # URLエンコードされたプロンプトを含むGemini URLを生成
    import urllib.parse
    encoded_prompt = urllib.parse.quote(prompt_text)
    gemini_url = f"https://gemini.google.com/app?q={encoded_prompt}"
    
    # JavaScriptでGeminiを新しいタブで開く
    st.markdown(f"""
    <script>
        window.open('{gemini_url}', '_blank');
    </script>
    """, unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🚀 新規プロダクト開発</h1>
    <p style="color: #94a3b8;">AIアシスタントと共に、次世代のプロダクトを創造しましょう</p>
</div>
""", unsafe_allow_html=True)

# ステップインジケーター
steps = ["アイデア", "リサーチ", "技術選定", "機能設計", "戦略", "確認"]
st.markdown('<div class="step-indicator">', unsafe_allow_html=True)
cols = st.columns(6)
for i, (col, step_name) in enumerate(zip(cols, steps)):
    with col:
        step_num = i + 1
        if step_num < st.session_state.new_product_step:
            status = "completed"
        elif step_num == st.session_state.new_product_step:
            status = "active"
        else:
            status = ""
        
        st.markdown(f"""
        <div class="step {status}">
            {step_num}
        </div>
        <div style="text-align: center; margin-top: 10px; color: #94a3b8; font-size: 0.9rem;">
            {step_name}
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# メインコンテンツ
if st.session_state.new_product_step == 1:
    # ステップ1: アイデア生成
    st.markdown(f"""
    <div class="gemini-card">
        <h2 style="color: white; margin-bottom: 20px;">💡 Gemini でプロダクトアイデアを生成</h2>
        <p style="color: #94a3b8; margin-bottom: 30px;">
            専用のGemがプロダクト情報を構造化してくれます
        </p>
        <a href="{GEMINI_GEMS_LINKS['product_structure']}" target="_blank" class="gemini-button">
            プロダクト構造化 Gem を開く →
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📝 アイデア入力フォーム")
    
    # プロンプト生成ボタンエリア
    prompt_col1, prompt_col2 = st.columns([1, 3])
    with prompt_col1:
        if st.button("💡 プロンプト生成", key="gen_prompt_idea", help="入力支援プロンプトを生成"):
            st.session_state.show_prompt_idea = True
    with prompt_col2:
        if st.button("🤖 Geminiで相談", key="open_gemini_idea", type="primary", help="Geminiを新しいタブで開く"):
            prompt = generate_prompt("product_idea", {"category": "新製品"})
            # URLを生成してコピー可能にする
            import urllib.parse
            encoded_prompt = urllib.parse.quote(prompt)
            gemini_url = f"https://gemini.google.com/app?q={encoded_prompt}"
            st.markdown(f'<a href="{gemini_url}" target="_blank">Geminiを開く（クリック）</a>', unsafe_allow_html=True)
            st.session_state.generated_prompts['product_idea'] = prompt
    
    # プロンプト表示エリア
    if st.session_state.get('show_prompt_idea', False):
        with st.expander("💡 生成されたプロンプト", expanded=True):
            prompt = generate_prompt("product_idea", {"category": "新製品"})
            st.code(prompt, language="text")
            if st.button("コピーしました", key="copy_prompt_idea"):
                st.success("プロンプトをコピーしました！Geminiに貼り付けてください。")
    
    with st.form("product_idea_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input(
                "プロダクト名 *",
                placeholder="例: TaskFlow AI",
                help="覚えやすく、ブランド化しやすい名前を選びましょう"
            )
            
            product_category = st.selectbox(
                "カテゴリ *",
                ["SaaS/ソフトウェア", "モバイルアプリ", "Webサービス", "AI/ML製品", 
                 "ハードウェア", "コンテンツ/メディア", "教育", "その他"]
            )
            
            target_audience = st.text_area(
                "ターゲットオーディエンス *",
                placeholder="例: 中小企業のマーケティング担当者、20-40代、デジタルツールに慣れている",
                height=100
            )
        
        with col2:
            problem_statement = st.text_area(
                "解決する課題 *",
                placeholder="例: マーケティング施策の効果測定が複雑で時間がかかる",
                height=100
            )
            
            unique_value = st.text_area(
                "独自の価値提案 *",
                placeholder="例: AIが自動で最適な施策を提案し、実行から分析まで一貫して行える",
                height=100
            )
        
        st.markdown("""
        <div class="hint-box">
            <div class="hint-title">💡 ヒント</div>
            <div>Gemini Gemsで以下のプロンプトを試してみてください：</div>
            <ul style="margin-top: 10px; margin-bottom: 0;">
                <li>「[ターゲット]向けの[カテゴリ]製品のアイデアを10個提案して」</li>
                <li>「[課題]を解決する革新的なソリューションを考えて」</li>
                <li>「[競合製品]の弱点を改善した新製品のコンセプトを作って」</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.form_submit_button("次のステップへ →", type="primary", use_container_width=True):
            if product_name and problem_statement and unique_value:
                st.session_state.product_draft.update({
                    "name": product_name,
                    "category": product_category,
                    "target_audience": target_audience,
                    "problem_statement": problem_statement,
                    "unique_value": unique_value
                })
                st.session_state.new_product_step = 2
                st.rerun()
            else:
                st.error("必須項目（*）をすべて入力してください")

elif st.session_state.new_product_step == 2:
    # ステップ2: 市場リサーチ
    st.markdown("### 🔍 市場リサーチ")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="gemini-card" style="padding: 20px;">
            <h3 style="color: white; margin-bottom: 15px;">📊 市場分析 Gem</h3>
            <a href="{GEMINI_GEMS_LINKS['market_analysis']}" target="_blank" class="gemini-button" style="font-size: 1rem; padding: 10px 20px;">
                市場分析を開始 →
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="gemini-card" style="padding: 20px;">
            <h3 style="color: white; margin-bottom: 15px;">🎯 競合分析 Gem</h3>
            <a href="{GEMINI_GEMS_LINKS['competitor_analysis']}" target="_blank" class="gemini-button" style="font-size: 1rem; padding: 10px 20px;">
                競合分析を開始 →
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # プロンプト生成ボタン
    st.markdown("#### 🤖 AI分析アシスタント")
    prompt_cols = st.columns(3)
    
    with prompt_cols[0]:
        if st.button("💡 市場分析プロンプト", key="gen_market", use_container_width=True):
            st.session_state.show_market_prompt = True
    
    with prompt_cols[1]:
        if st.button("👥 ペルソナ分析プロンプト", key="gen_persona", use_container_width=True):
            st.session_state.show_persona_prompt = True
    
    with prompt_cols[2]:
        if st.button("🏢 競合分析プロンプト", key="gen_competitor", use_container_width=True):
            st.session_state.show_competitor_prompt = True
    
    # プロンプト表示
    if st.session_state.get('show_market_prompt', False):
        with st.expander("📊 市場分析プロンプト", expanded=True):
            context = {"product_name": st.session_state.product_draft.get('name', '新製品')}
            prompt = generate_prompt("market_analysis", context)
            st.code(prompt, language="text")
            st.info("このプロンプトをコピーしてGeminiに貼り付けてください")
    
    if st.session_state.get('show_persona_prompt', False):
        with st.expander("👥 ペルソナ分析プロンプト", expanded=True):
            context = {"product_name": st.session_state.product_draft.get('name', '新製品')}
            prompt = generate_prompt("target_persona", context)
            st.code(prompt, language="text")
            st.info("このプロンプトをコピーしてGeminiに貼り付けてください")
    
    if st.session_state.get('show_competitor_prompt', False):
        with st.expander("🏢 競合分析プロンプト", expanded=True):
            prompt = f"""「{st.session_state.product_draft.get('name', '新製品')}」の競合分析を行ってください：

【競合マッピング】
直接競合（3社）:
1. 企業名 - 製品名 - 強み/弱み
2. 企業名 - 製品名 - 強み/弱み
3. 企業名 - 製品名 - 強み/弱み

間接競合（2社）:
1. 企業名 - 代替ソリューション
2. 企業名 - 代替ソリューション

【差別化ポイント】
自社が勝てる領域:
1. 
2. 
3. """
            st.code(prompt, language="text")
            st.info("このプロンプトをコピーしてGeminiに貼り付けてください")
    
    with st.form("market_research_form"):
        st.subheader("リサーチ結果入力")
        
        col1, col2 = st.columns(2)
        
        with col1:
            market_size = st.text_input(
                "市場規模",
                placeholder="例: 国内500億円、年成長率15%"
            )
            
            main_competitors = st.text_area(
                "主要競合（3-5社）",
                placeholder="例:\n- Notion (月額$8-)\n- Asana (月額$10.99-)\n- Monday.com (月額$8-)",
                height=120
            )
            
            market_trends = st.text_area(
                "市場トレンド",
                placeholder="例:\n- AI活用の需要増加\n- リモートワーク対応\n- 統合プラットフォーム化",
                height=120
            )
        
        with col2:
            target_persona = st.text_area(
                "詳細ペルソナ",
                placeholder="例:\n年齢: 25-40歳\n職種: マーケター、プロダクトマネージャー\n課題: 複数ツールの管理が煩雑\n期待: 一元化と自動化",
                height=120
            )
            
            competitive_advantage = st.text_area(
                "競合優位性",
                placeholder="例:\n- AI自動化機能\n- 日本市場特化\n- 直感的UI\n- 手厚いサポート",
                height=120
            )
        
        if st.form_submit_button("次のステップへ →", type="primary", use_container_width=True):
            st.session_state.product_draft.update({
                "market_size": market_size,
                "main_competitors": main_competitors,
                "market_trends": market_trends,
                "target_persona": target_persona,
                "competitive_advantage": competitive_advantage
            })
            st.session_state.new_product_step = 3
            st.rerun()

elif st.session_state.new_product_step == 3:
    # ステップ3: 技術スタック選定
    st.markdown("### 💻 技術スタック選定")
    
    st.markdown(f"""
    <div class="gemini-card">
        <h3 style="color: white; margin-bottom: 15px;">🛠️ 技術スタック選定アシスタント</h3>
        <p style="color: #94a3b8; margin-bottom: 20px;">
            プロジェクトに最適な技術構成を提案します
        </p>
        <a href="{GEMINI_GEMS_LINKS['tech_stack']}" target="_blank" class="gemini-button">
            技術スタック選定 Gem を開く →
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # プロンプトテンプレート表示
    with st.expander("📋 AIプロンプトテンプレート", expanded=True):
        st.info("以下のテンプレートをGemに貼り付けて、技術スタックを決定してください")
        
        template = f"""あなたはプロのAIプロンプトエンジニアです。
私は非エンジニアでプロンプトエンジニアリングも初心者です。

以下のプロジェクトの技術スタックを選定するのを手伝ってください：

【プロジェクト概要】
- 製品名: {st.session_state.product_draft.get('name', '[製品名]')}
- カテゴリ: {st.session_state.product_draft.get('category', '[カテゴリ]')}
- ターゲット: {st.session_state.product_draft.get('target_audience', '[ターゲット]')}
- 解決する課題: {st.session_state.product_draft.get('problem_statement', '[課題]')}

【基本テンプレート】
```
【プロジェクト名】: {st.session_state.product_draft.get('name', '[最後に決める]')}
【プロジェクトパス】: ~/AIOrganize/tmp/projects/[最後に決める]

【技術スタック】
- フロントエンド: [ここ埋める]
- バックエンド: [ここ埋める]
- データベース: [ここ埋める]
- デプロイ: [ここ埋める]

【機能要件】
- [ここ埋める]
- [ここ埋める]
- [ここ埋める]

【品質要件】
- [ここ埋める]
- [ここ埋める]
```

私の要望：
- 個人開発なので、シンプルで管理しやすいものが良い
- スピード重視で開発したい
- 将来的にスケールできる構成

質問と提案をして、一つずつ確実に決めていってください。"""
        
        st.code(template, language="text")
    
    with st.form("tech_stack_form"):
        st.subheader("技術構成の決定")
        
        # 技術スタック入力
        col1, col2 = st.columns(2)
        
        with col1:
            frontend_input = st.text_input(
                "フロントエンド技術",
                placeholder="例: Next.js + TypeScript + TailwindCSS",
                help="Gemで決定した技術を入力"
            )
            
            backend_input = st.text_input(
                "バックエンド技術",
                placeholder="例: Python FastAPI",
                help="Gemで決定した技術を入力"
            )
            
            database_input = st.text_input(
                "データベース",
                placeholder="例: PostgreSQL + Redis",
                help="Gemで決定した技術を入力"
            )
            
            deploy_input = st.text_input(
                "デプロイ環境",
                placeholder="例: Vercel + AWS",
                help="Gemで決定した技術を入力"
            )
        
        with col2:
            # 機能要件
            st.markdown("#### 主要機能要件")
            functional_requirements = st.text_area(
                "機能要件（箇条書き）",
                placeholder="例:\n- ユーザー認証\n- リアルタイムデータ同期\n- API連携",
                height=150,
                help="Gemで整理した機能要件を入力"
            )
            
            # 品質要件
            st.markdown("#### 品質要件")
            quality_requirements = st.text_area(
                "品質要件（箇条書き）",
                placeholder="例:\n- レスポンス速度 < 200ms\n- 99.9%アップタイム\n- モバイル対応",
                height=100,
                help="Gemで整理した品質要件を入力"
            )
        
        # プロジェクトパス
        project_path = st.text_input(
            "プロジェクトパス名（英語）",
            placeholder="例: marketing-flow-dashboard",
            help="プロジェクトフォルダ名を英語で入力"
        )
        
        if st.form_submit_button("次のステップへ →", type="primary", use_container_width=True):
            if frontend_input and backend_input and database_input and deploy_input:
                st.session_state.product_draft.update({
                    "frontend_stack": frontend_input,
                    "backend_stack": backend_input,
                    "database_stack": database_input,
                    "deploy_stack": deploy_input,
                    "functional_requirements": functional_requirements,
                    "quality_requirements": quality_requirements,
                    "project_path": project_path or "new-project"
                })
                st.session_state.new_product_step = 4
                st.rerun()
            else:
                st.error("技術スタックをすべて入力してください")

elif st.session_state.new_product_step == 4:
    # ステップ4: 機能設計
    st.markdown("### 🛠️ 機能設計")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="gemini-card">
            <h3 style="color: white; margin-bottom: 15px;">🎨 機能設計アシスタント</h3>
            <p style="color: #94a3b8; margin-bottom: 20px;">
                機能から価値への変換を支援
            </p>
            <a href="{GEMINI_GEMS_LINKS['benefit_extraction']}" target="_blank" class="gemini-button" style="font-size: 1rem; padding: 10px 30px;">
                ベネフィット抽出 Gem →
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="gemini-card">
            <h3 style="color: white; margin-bottom: 15px;">📝 コンテンツ生成</h3>
            <p style="color: #94a3b8; margin-bottom: 20px;">
                マーケティングコンテンツ作成
            </p>
            <a href="{GEMINI_GEMS_LINKS['content_generation']}" target="_blank" class="gemini-button" style="font-size: 1rem; padding: 10px 30px;">
                コンテンツ生成 Gem →
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # プロンプト生成ボタン
    if st.button("💡 MVP機能設計プロンプト", key="gen_mvp", use_container_width=True):
        st.session_state.show_mvp_prompt = True
    
    if st.session_state.get('show_mvp_prompt', False):
        with st.expander("🚀 MVP機能設計プロンプト", expanded=True):
            context = {"product_name": st.session_state.product_draft.get('name', '新製品')}
            prompt = generate_prompt("mvp_features", context)
            st.code(prompt, language="text")
            st.info("このプロンプトをコピーしてGeminiに貼り付けてください")
    
    with st.form("feature_design_form"):
        st.subheader("主要機能の定義")
        
        # MVPの機能
        st.markdown("#### 🚀 MVP機能（最初のリリース）")
        mvp_features = st.text_area(
            "必須機能リスト",
            placeholder="例:\n- ユーザー認証\n- ダッシュボード\n- 基本的なタスク管理\n- 通知機能",
            height=150
        )
        
        # 将来の機能
        st.markdown("#### 🎯 将来の拡張機能")
        future_features = st.text_area(
            "フェーズ2以降の機能",
            placeholder="例:\n- AI予測分析\n- 外部サービス連携\n- モバイルアプリ\n- エンタープライズ機能",
            height=150
        )
        
        # 技術スタック
        st.markdown("#### 💻 技術スタック")
        col1, col2 = st.columns(2)
        
        with col1:
            frontend_tech = st.multiselect(
                "フロントエンド",
                ["React", "Vue.js", "Angular", "Next.js", "Svelte", "その他"],
                default=["Next.js"]
            )
            
            backend_tech = st.multiselect(
                "バックエンド",
                ["Node.js", "Python", "Ruby", "Go", "Java", "その他"],
                default=["Python"]
            )
        
        with col2:
            database = st.multiselect(
                "データベース",
                ["PostgreSQL", "MySQL", "MongoDB", "Firebase", "Supabase", "その他"],
                default=["PostgreSQL"]
            )
            
            hosting = st.multiselect(
                "ホスティング",
                ["AWS", "Google Cloud", "Azure", "Vercel", "Heroku", "その他"],
                default=["Vercel"]
            )
        
        if st.form_submit_button("次のステップへ →", type="primary", use_container_width=True):
            st.session_state.product_draft.update({
                "mvp_features": mvp_features,
                "future_features": future_features
            })
            st.session_state.new_product_step = 5
            st.rerun()

elif st.session_state.new_product_step == 5:
    # ステップ5: ビジネス戦略
    st.markdown("### 💰 ビジネス戦略")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="gemini-card" style="padding: 20px;">
            <h3 style="color: white; margin-bottom: 15px;">💵 価格戦略 Gem</h3>
            <a href="https://gemini.google.com/gems" target="_blank" class="gemini-button" style="font-size: 1rem; padding: 10px 20px;">
                価格戦略を検討 →
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="gemini-card" style="padding: 20px;">
            <h3 style="color: white; margin-bottom: 15px;">📈 成長戦略 Gem</h3>
            <a href="https://gemini.google.com/gems" target="_blank" class="gemini-button" style="font-size: 1rem; padding: 10px 20px;">
                成長戦略を策定 →
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # プロンプト生成ボタン
    if st.button("💡 価格戦略プロンプト", key="gen_pricing", use_container_width=True):
        st.session_state.show_pricing_prompt = True
    
    if st.session_state.get('show_pricing_prompt', False):
        with st.expander("💰 価格戦略プロンプト", expanded=True):
            context = {"product_name": st.session_state.product_draft.get('name', '新製品')}
            prompt = generate_prompt("pricing_strategy", context)
            st.code(prompt, language="text")
            st.info("このプロンプトをコピーしてGeminiに貼り付けてください")
    
    with st.form("business_strategy_form"):
        st.subheader("ビジネスモデル設計")
        
        # 価格プラン
        st.markdown("#### 💳 価格プラン")
        pricing_model = st.selectbox(
            "価格モデル",
            ["フリーミアム", "サブスクリプション", "従量課金", "買い切り", "ハイブリッド"]
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            free_plan = st.text_area(
                "無料プラン",
                placeholder="例:\n- 3プロジェクトまで\n- 基本機能のみ\n- コミュニティサポート",
                height=120
            )
        
        with col2:
            pro_plan = st.text_area(
                "プロプラン",
                placeholder="例:\n月額¥2,980\n- 無制限プロジェクト\n- AI機能\n- 優先サポート",
                height=120
            )
        
        with col3:
            enterprise_plan = st.text_area(
                "エンタープライズ",
                placeholder="例:\n要見積もり\n- カスタマイズ可能\n- SLA保証\n- 専任サポート",
                height=120
            )
        
        # マーケティング戦略
        st.markdown("#### 📣 Go-to-Market戦略")
        
        launch_strategy = st.text_area(
            "ローンチ戦略",
            placeholder="例:\n1. プライベートベータ（100名限定）\n2. Product Hunt掲載\n3. インフルエンサーマーケティング\n4. コンテンツマーケティング",
            height=150
        )
        
        success_metrics = st.text_area(
            "成功指標（KPI）",
            placeholder="例:\n- 3ヶ月で1000ユーザー獲得\n- 月間アクティブ率60%以上\n- 有料転換率5%\n- NPS 50以上",
            height=120
        )
        
        if st.form_submit_button("最終確認へ →", type="primary", use_container_width=True):
            st.session_state.product_draft.update({
                "pricing_model": pricing_model,
                "free_plan": free_plan,
                "pro_plan": pro_plan,
                "enterprise_plan": enterprise_plan,
                "launch_strategy": launch_strategy,
                "success_metrics": success_metrics
            })
            st.session_state.new_product_step = 6
            st.rerun()

elif st.session_state.new_product_step == 6:
    # ステップ6: 最終確認
    st.markdown("### ✅ プロダクト開発計画の確認")
    
    # サマリー表示
    st.markdown("""
    <div class="form-section">
        <h2 class="section-title">
            <span class="section-icon">📋</span>
            プロダクトサマリー
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    draft = st.session_state.product_draft
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 基本情報")
        st.info(f"**製品名**: {draft.get('name', 'N/A')}")
        st.info(f"**カテゴリ**: {draft.get('category', 'N/A')}")
        st.info(f"**価格モデル**: {draft.get('pricing_model', 'N/A')}")
        
        st.markdown("#### 市場情報")
        st.info(f"**市場規模**: {draft.get('market_size', 'N/A')}")
        st.info(f"**ターゲット**: {draft.get('target_audience', 'N/A')}")
    
    with col2:
        st.markdown("#### 解決する課題")
        st.warning(draft.get('problem_statement', 'N/A'))
        
        st.markdown("#### 独自の価値")
        st.success(draft.get('unique_value', 'N/A'))
    
    # 詳細情報
    with st.expander("📊 詳細情報を表示"):
        st.markdown("**主要競合**")
        st.text(draft.get('main_competitors', 'N/A'))
        
        st.markdown("**MVP機能**")
        st.text(draft.get('mvp_features', 'N/A'))
        
        st.markdown("**技術スタック**")
        tech_stack = f"""
        - フロントエンド: {draft.get('frontend_stack', 'N/A')}
        - バックエンド: {draft.get('backend_stack', 'N/A')}
        - データベース: {draft.get('database_stack', 'N/A')}
        - デプロイ: {draft.get('deploy_stack', 'N/A')}
        """
        st.text(tech_stack)
        
        st.markdown("**機能要件**")
        st.text(draft.get('functional_requirements', 'N/A'))
        
        st.markdown("**品質要件**")
        st.text(draft.get('quality_requirements', 'N/A'))
    
    # アクションボタン
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 編集する", use_container_width=True):
            st.session_state.new_product_step = 1
            st.rerun()
    
    with col2:
        if st.button("💾 下書き保存", use_container_width=True):
            st.success("下書きを保存しました")
    
    with col3:
        if st.button("🚀 プロジェクト作成", type="primary", use_container_width=True):
            # プロジェクトを作成してフローダッシュボードに移動
            if 'projects' not in st.session_state:
                st.session_state.projects = {}
            
            project_id = f"project_{len(st.session_state.projects) + 1}"
            st.session_state.projects[project_id] = {
                'id': project_id,
                'name': draft.get('name', '新規プロダクト'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'flow_stage': 0,
                'flow_data': {
                    'product_info': {
                        'name': draft.get('name'),
                        'category': draft.get('category'),
                        'target': draft.get('target_audience'),
                        'price': draft.get('pro_plan', '未定'),
                        'uniqueness': draft.get('unique_value')
                    }
                },
                'competitive_analysis': {
                    'market_size': draft.get('market_size'),
                    'competitors': draft.get('main_competitors', '').split('\n'),
                    'market_trends': draft.get('market_trends', '').split('\n'),
                    'competitive_advantage': draft.get('competitive_advantage', '').split('\n')
                }
            }
            
            if 'project_order' not in st.session_state:
                st.session_state.project_order = []
            st.session_state.project_order.append(project_id)
            
            st.session_state.current_project_id = project_id
            st.session_state.flow_stage = 0
            
            # 下書きをクリア
            st.session_state.product_draft = {}
            st.session_state.new_product_step = 1
            
            st.success("プロジェクトを作成しました！")
            st.switch_page("pages/development_room.py")

# サイドバー
with st.sidebar:
    st.header("🚀 プロダクト開発ガイド")
    
    st.markdown("""
    ### 開発フロー
    
    1. **アイデア生成** 
       - Gemini Gemsでブレスト
       - 課題と価値を明確化
    
    2. **市場リサーチ**
       - 競合分析
       - ターゲット調査
    
    3. **機能設計**
       - MVP定義
       - 技術選定
    
    4. **ビジネス戦略**
       - 価格設定
       - 成長計画
    
    5. **プロジェクト開始**
       - 計画確認
       - 実行開始
    """)
    
    st.markdown("---")
    
    st.header("💡 専用Gemini Gems")
    
    gems = [
        {"name": "プロダクト構造化", "url": GEMINI_GEMS_LINKS['product_structure'], "desc": "製品情報を整理"},
        {"name": "市場分析", "url": GEMINI_GEMS_LINKS['market_analysis'], "desc": "市場機会の発見"},
        {"name": "競合分析", "url": GEMINI_GEMS_LINKS['competitor_analysis'], "desc": "競合状況の把握"},
        {"name": "技術スタック選定", "url": GEMINI_GEMS_LINKS['tech_stack'], "desc": "最適な技術構成"},
        {"name": "ベネフィット抽出", "url": GEMINI_GEMS_LINKS['benefit_extraction'], "desc": "価値提案の明確化"},
        {"name": "コンテンツ生成", "url": GEMINI_GEMS_LINKS['content_generation'], "desc": "マーケティング素材作成"}
    ]
    
    for gem in gems:
        st.markdown(f"""
        <a href="{gem['url']}" target="_blank" style="text-decoration: none;">
            <button style="width: 100%; padding: 10px; margin-bottom: 10px; background: rgba(59, 130, 246, 0.1); 
                           border: 1px solid #3b82f6; color: white; border-radius: 8px; cursor: pointer;">
                🔗 {gem['name']}
                <br><small style="color: #94a3b8;">{gem['desc']}</small>
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("⬅️ ホームに戻る", type="secondary", use_container_width=True):
        st.switch_page("pages/../home.py")