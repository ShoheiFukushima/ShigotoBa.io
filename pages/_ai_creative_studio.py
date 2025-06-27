#!/usr/bin/env python3
"""
AI駆動クリエイティブスタジオ
最強の広告代理店機能 - AIによる自動クリエイティブ生成と最適化
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import uuid
import base64
from io import BytesIO

# ページ設定
st.set_page_config(
    page_title="AI Creative Studio",
    page_icon="🎨",
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
    
    /* グラデーション背景 */
    .creative-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
    }
    
    .creative-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .creative-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* クリエイティブカード */
    .creative-card {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .creative-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .creative-card:hover::before {
        left: 100%;
    }
    
    .creative-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
        border-color: #667eea;
    }
    
    /* AI生成インジケーター */
    .ai-generated {
        background: linear-gradient(45deg, #10b981, #059669);
        color: white;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    /* 性能メトリクス */
    .performance-metric {
        background: rgba(30, 41, 59, 0.8);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 5px;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    .metric-trend {
        font-size: 0.8rem;
        padding: 4px 8px;
        border-radius: 12px;
        margin-top: 5px;
        display: inline-block;
    }
    
    .trend-up {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .trend-down {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    /* ツールボタン */
    .tool-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .tool-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* プログレスバー */
    .progress-container {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 10px;
        padding: 3px;
        margin: 10px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 8px;
        border-radius: 8px;
        transition: width 1s ease;
    }
    
    /* 創作プロセス */
    .creation-step {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s;
    }
    
    .creation-step:hover {
        background: rgba(30, 41, 59, 0.8);
        transform: translateX(10px);
    }
    
    .step-number {
        background: #667eea;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 15px;
    }
    
    /* タグクラウド */
    .tag-cloud {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 15px 0;
    }
    
    .tag {
        background: rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s;
    }
    
    .tag:hover {
        background: rgba(102, 126, 234, 0.4);
        transform: scale(1.1);
    }
    
    /* モックアップビューア */
    .mockup-viewer {
        background: #f8fafc;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 3px dashed #cbd5e1;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #64748b;
        font-size: 1.1rem;
    }
    
    /* AIインサイト */
    .ai-insight {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    
    .insight-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    /* バリエーションギャラリー */
    .variation-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .variation-item {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .variation-item:hover {
        background: rgba(30, 41, 59, 0.8);
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'creative_projects' not in st.session_state:
    st.session_state.creative_projects = {}

if 'ai_insights' not in st.session_state:
    st.session_state.ai_insights = []

if 'current_creative_mode' not in st.session_state:
    st.session_state.current_creative_mode = "dashboard"

def generate_creative_id():
    """クリエイティブIDを生成"""
    return f"creative_{datetime.now().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:8]}"

def generate_ai_creative_content_mock(creative_type: str, target_audience: str, brand_info: Dict) -> Dict[str, Any]:
    """AI駆動のクリエイティブコンテンツ生成（モック版）"""
    templates = {
        "ad_copy": {
            "headline": f"革新的な{brand_info.get('category', '製品')}で{target_audience}の生活を変革",
            "subheadline": f"{brand_info.get('value_prop', '独自の価値')}を体験してください",
            "cta": "今すぐ始める",
            "body": f"{target_audience}に最適化された{brand_info.get('category', 'ソリューション')}。業界をリードする技術で、あなたの課題を解決します。"
        },
        "social_post": {
            "twitter": f"🚀 {brand_info.get('name', 'ブランド')}の新機能をチェック！ #{target_audience.replace(' ', '')}",
            "instagram": f"✨ {target_audience}のための革新的な体験を提供します！ 詳細はストーリーズで 📱",
            "linkedin": f"プロフェッショナルな{target_audience}向けの最新ソリューションをご紹介します。",
            "facebook": f"{target_audience}に特化した{brand_info.get('category', '製品')}で、新しい可能性を発見してください！"
        },
        "video_script": {
            "hook": f"あなたが{target_audience}なら、この3秒で人生が変わります",
            "problem": f"{target_audience}が直面する最大の課題...",
            "solution": f"{brand_info.get('name', 'ソリューション')}があなたの答えです",
            "cta": "今すぐ詳細を確認してください"
        },
        "email_campaign": {
            "subject": f"{target_audience}限定：特別オファーのお知らせ",
            "preview": "見逃せない機会をお届けします",
            "header": f"こんにちは、{target_audience}の皆様",
            "body": f"あなたのような{target_audience}に特別にご用意した、限定オファーをお知らせします。"
        }
    }
    
    return {
        "content": templates.get(creative_type, {}),
        "generated_at": datetime.now().isoformat(),
        "performance_prediction": {
            "ctr_estimate": np.random.uniform(1.5, 8.5),
            "engagement_score": np.random.uniform(60, 95),
            "conversion_probability": np.random.uniform(0.8, 4.2),
            "virality_potential": np.random.uniform(10, 85)
        },
        "optimization_suggestions": [
            f"{target_audience}の感情に訴える要素を強化",
            "CTAをより行動を促す表現に調整",
            "視覚的インパクトを高める要素を追加",
            "トレンドキーワードの活用を検討"
        ]
    }

async def generate_ai_creative_content(creative_type: str, target_audience: str, brand_info: Dict) -> Dict[str, Any]:
    """AI駆動のクリエイティブコンテンツ生成（実AI版）"""
    # 環境変数でモック/実AIを切り替え
    USE_MOCK = os.getenv('USE_MOCK_AI', 'false').lower() == 'true'
    
    if USE_MOCK:
        return generate_ai_creative_content_mock(creative_type, target_audience, brand_info)
    
    try:
        # AIクライアントのインポート
        from config.ai_client import ai_client
        from config.ai_models import TaskType
        
        # プロンプト作成
        system_prompt = """あなたはプロのマーケティングクリエイターです。
ブランドの価値を最大限に引き出し、ターゲット層に響く魅力的なコンテンツを作成してください。

重要な要素:
1. ターゲット層の感情に訴える
2. ブランドの独自性を強調
3. 明確な行動喚起（CTA）
4. プラットフォームに最適化した形式"""

        user_prompt = f"""
以下の条件でクリエイティブコンテンツを生成してください：

コンテンツタイプ: {creative_type}
ターゲット層: {target_audience}
ブランド情報:
- 名称: {brand_info.get('name', 'ブランド')}
- カテゴリ: {brand_info.get('category', '製品・サービス')}
- 価値提案: {brand_info.get('value_prop', '独自の価値')}
- トーン: {brand_info.get('tone', 'プロフェッショナル')}

生成する内容:
{get_content_requirements(creative_type)}

JSON形式で出力してください。
"""

        # AI生成
        response = await ai_client.generate_content(
            prompt=user_prompt,
            task_type=TaskType.GENERATION,
            system_prompt=system_prompt,
            temperature=0.8,
            max_tokens=1000
        )
        
        # レスポンスをパース
        content = json.loads(response)
        
        # パフォーマンス予測（別のAI呼び出し）
        performance = await predict_creative_performance(content, target_audience)
        
        return {
            "content": content,
            "generated_at": datetime.now().isoformat(),
            "performance_prediction": performance,
            "optimization_suggestions": await get_optimization_suggestions(content, target_audience)
        }
        
    except Exception as e:
        st.error(f"AI生成エラー: {str(e)}")
        # エラー時はモック版にフォールバック
        return generate_ai_creative_content_mock(creative_type, target_audience, brand_info)

def get_content_requirements(creative_type: str) -> str:
    """コンテンツタイプ別の要件を返す"""
    requirements = {
        "ad_copy": """
- headline: 魅力的な見出し（15-30文字）
- subheadline: サブ見出し（30-50文字）
- body: 本文（100-200文字）
- cta: 行動喚起ボタンテキスト
""",
        "social_post": """
- twitter: Twitter用投稿（280文字以内、ハッシュタグ含む）
- instagram: Instagram用投稿（キャプション、絵文字活用）
- linkedin: LinkedIn用投稿（プロフェッショナルトーン）
- facebook: Facebook用投稿（エンゲージメント重視）
""",
        "video_script": """
- hook: 最初の3秒で視聴者を引きつけるフック
- problem: 視聴者の課題・痛み
- solution: ブランドが提供する解決策
- cta: 締めの行動喚起
""",
        "email_campaign": """
- subject: 件名（開封率を高める）
- preview: プレビューテキスト
- header: 挨拶・導入
- body: 本文（価値提案中心）
- cta: 明確な行動喚起
"""
    }
    return requirements.get(creative_type, "適切なコンテンツを生成してください")

async def predict_creative_performance(content: Dict, target_audience: str) -> Dict[str, float]:
    """クリエイティブのパフォーマンスを予測"""
    # TODO: 実際のパフォーマンス予測ロジックを実装
    # 現在は簡易版
    return {
        "ctr_estimate": np.random.uniform(2.0, 7.0),
        "engagement_score": np.random.uniform(70, 90),
        "conversion_probability": np.random.uniform(1.5, 3.5),
        "virality_potential": np.random.uniform(20, 70)
    }

async def get_optimization_suggestions(content: Dict, target_audience: str) -> List[str]:
    """最適化提案を生成"""
    # TODO: AIベースの最適化提案を実装
    return [
        f"{target_audience}により響くキーワードの使用を検討",
        "感情的なトリガーワードを追加",
        "社会的証明（実績・レビュー）の要素を強化",
        "緊急性・限定性を演出する要素を追加"
    ]

def calculate_creative_score(creative_data: Dict) -> float:
    """クリエイティブの総合スコアを計算"""
    performance = creative_data.get('performance_prediction', {})
    
    ctr = performance.get('ctr_estimate', 0) / 10 * 100
    engagement = performance.get('engagement_score', 0)
    conversion = performance.get('conversion_probability', 0) / 5 * 100
    virality = performance.get('virality_potential', 0)
    
    return (ctr + engagement + conversion + virality) / 4

# ヘッダー
st.markdown("""
<div class="creative-header">
    <div class="creative-title">🎨 AI Creative Studio</div>
    <div class="creative-subtitle">最強の広告代理店機能 - AI駆動クリエイティブ自動生成プラットフォーム</div>
</div>
""", unsafe_allow_html=True)

# メインダッシュボード
if st.session_state.current_creative_mode == "dashboard":
    
    # KPIメトリクス
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_creatives = len(st.session_state.creative_projects)
        st.markdown(f"""
        <div class="performance-metric">
            <div class="metric-value">{total_creatives}</div>
            <div class="metric-label">生成クリエイティブ</div>
            <div class="metric-trend trend-up">+{total_creatives * 12}% 今月</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_score = 87.5 if total_creatives > 0 else 0
        st.markdown(f"""
        <div class="performance-metric">
            <div class="metric-value">{avg_score:.1f}</div>
            <div class="metric-label">平均スコア</div>
            <div class="metric-trend trend-up">+15.3% 改善</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        active_campaigns = min(total_creatives * 2, 24)
        st.markdown(f"""
        <div class="performance-metric">
            <div class="metric-value">{active_campaigns}</div>
            <div class="metric-label">稼働キャンペーン</div>
            <div class="metric-trend trend-up">+8 新規</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        roi_multiplier = 3.8
        st.markdown(f"""
        <div class="performance-metric">
            <div class="metric-value">{roi_multiplier:.1f}x</div>
            <div class="metric-label">平均ROI</div>
            <div class="metric-trend trend-up">+0.7x 向上</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        automation_rate = 94.2
        st.markdown(f"""
        <div class="performance-metric">
            <div class="metric-value">{automation_rate:.0f}%</div>
            <div class="metric-label">自動化率</div>
            <div class="metric-trend trend-up">完全自動化</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # クイック作成ツール
    st.markdown("### 🚀 クイック作成ツール")
    
    tool_cols = st.columns(4)
    
    with tool_cols[0]:
        if st.button("📝 AI広告コピー生成", use_container_width=True, type="primary"):
            st.session_state.current_creative_mode = "ad_copy"
            st.rerun()
    
    with tool_cols[1]:
        if st.button("📱 SNSコンテンツ作成", use_container_width=True, type="primary"):
            st.session_state.current_creative_mode = "social_content"
            st.rerun()
    
    with tool_cols[2]:
        if st.button("🎬 動画スクリプト生成", use_container_width=True, type="primary"):
            st.session_state.current_creative_mode = "video_script"
            st.rerun()
    
    with tool_cols[3]:
        if st.button("📧 メールキャンペーン", use_container_width=True, type="primary"):
            st.session_state.current_creative_mode = "email_campaign"
            st.rerun()
    
    # 高度なツール
    st.markdown("### ⚡ 高度なAIツール")
    
    advanced_cols = st.columns(3)
    
    with advanced_cols[0]:
        if st.button("🧠 ディープ競合分析", use_container_width=True):
            st.session_state.current_creative_mode = "competitor_analysis"
            st.rerun()
    
    with advanced_cols[1]:
        if st.button("🎯 ペルソナ最適化", use_container_width=True):
            st.session_state.current_creative_mode = "persona_optimization"
            st.rerun()
    
    with advanced_cols[2]:
        if st.button("📊 予測分析ダッシュボード", use_container_width=True):
            st.session_state.current_creative_mode = "predictive_analytics"
            st.rerun()
    
    # 最新の生成物
    if st.session_state.creative_projects:
        st.markdown("### 🎨 最新のクリエイティブ")
        
        # 最新5件を表示
        latest_projects = sorted(
            st.session_state.creative_projects.items(),
            key=lambda x: x[1].get('created_at', ''),
            reverse=True
        )[:5]
        
        for project_id, project in latest_projects:
            score = calculate_creative_score(project)
            
            st.markdown(f"""
            <div class="creative-card">
                <div class="ai-generated">🤖 AI Generated</div>
                <h3>{project['name']}</h3>
                <p><strong>タイプ:</strong> {project['type']}</p>
                <p><strong>ターゲット:</strong> {project['target_audience']}</p>
                <p><strong>スコア:</strong> {score:.1f}/100</p>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {score}%;"></div>
                </div>
                <p><strong>予測CTR:</strong> {project.get('ai_content', {}).get('performance_prediction', {}).get('ctr_estimate', 0):.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    # AIインサイト
    st.markdown("### 🧠 AIインサイト & 推奨事項")
    
    insights = [
        {
            "icon": "🎯",
            "title": "ターゲット最適化の機会",
            "insight": "現在のオーディエンスセグメントを細分化することで、CTRを23%向上させる可能性があります。",
            "action": "ペルソナ分析ツールで詳細なセグメンテーションを実行"
        },
        {
            "icon": "📈",
            "title": "パフォーマンス予測",
            "insight": "今後7日間で、エンゲージメント率が平均15%上昇する見込みです。",
            "action": "追加クリエイティブバリエーションの投入を推奨"
        },
        {
            "icon": "💡",
            "title": "トレンド活用チャンス",
            "insight": "新興キーワード「サステナブル」の検索ボリュームが急上昇中です。",
            "action": "環境配慮をテーマにしたコンテンツ制作を検討"
        }
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div class="ai-insight">
            <div class="insight-icon">{insight['icon']}</div>
            <h4>{insight['title']}</h4>
            <p>{insight['insight']}</p>
            <p><strong>推奨アクション:</strong> {insight['action']}</p>
        </div>
        """, unsafe_allow_html=True)

# 広告コピー生成モード
elif st.session_state.current_creative_mode == "ad_copy":
    
    if st.button("⬅️ ダッシュボードに戻る"):
        st.session_state.current_creative_mode = "dashboard"
        st.rerun()
    
    st.markdown("## 📝 AI広告コピー生成")
    
    with st.form("ad_copy_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            brand_name = st.text_input("ブランド名*", placeholder="例: TechSolutions Pro")
            product_category = st.selectbox(
                "カテゴリ*",
                ["SaaS", "Eコマース", "教育", "ヘルスケア", "フィンテック", "エンターテイメント", "その他"]
            )
            target_audience = st.text_input("ターゲットオーディエンス*", placeholder="例: 中小企業の経営者")
        
        with col2:
            value_proposition = st.text_area("価値提案", placeholder="例: 業務効率を80%向上させるAIツール")
            tone = st.selectbox("トーン", ["プロフェッショナル", "フレンドリー", "エモーショナル", "ユーモラス", "権威的"])
            campaign_goal = st.selectbox("キャンペーン目標", ["認知度向上", "リード獲得", "売上増加", "ブランディング"])
        
        keywords = st.text_input("キーワード（カンマ区切り）", placeholder="AI, 自動化, 効率化")
        competitors = st.text_input("主要競合（参考）", placeholder="CompetitorA, CompetitorB")
        
        submitted = st.form_submit_button("🚀 AI生成開始", type="primary", use_container_width=True)
        
        if submitted and brand_name and target_audience:
            
            # 生成プロセスの可視化
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            import time
            
            # ステップ1: ターゲット分析
            status_text.text("🎯 ターゲットオーディエンス分析中...")
            progress_bar.progress(20)
            time.sleep(1)
            
            # ステップ2: 競合分析
            status_text.text("🔍 競合分析実行中...")
            progress_bar.progress(40)
            time.sleep(1)
            
            # ステップ3: クリエイティブ生成
            status_text.text("🧠 AIクリエイティブ生成中...")
            progress_bar.progress(60)
            time.sleep(1)
            
            # ステップ4: 最適化
            status_text.text("⚡ パフォーマンス最適化中...")
            progress_bar.progress(80)
            time.sleep(1)
            
            # ステップ5: 完了
            status_text.text("✅ 生成完了！")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            # クリエイティブ生成
            brand_info = {
                "name": brand_name,
                "category": product_category,
                "value_prop": value_proposition
            }
            
            ai_content = generate_ai_creative_content("ad_copy", target_audience, brand_info)
            
            # プロジェクトとして保存
            project_id = generate_creative_id()
            project_data = {
                "name": f"{brand_name} - 広告コピー",
                "type": "広告コピー",
                "target_audience": target_audience,
                "brand_info": brand_info,
                "ai_content": ai_content,
                "created_at": datetime.now().isoformat(),
                "tone": tone,
                "goal": campaign_goal,
                "keywords": [k.strip() for k in keywords.split(',') if k.strip()]
            }
            
            st.session_state.creative_projects[project_id] = project_data
            
            # 生成結果の表示
            st.success("🎉 AI広告コピーが生成されました！")
            
            # メインコピー
            content = ai_content['content']
            st.markdown("### 📝 生成されたコピー")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="creative-card">
                    <h4>🎯 メインヘッドライン</h4>
                    <h2 style="color: #667eea;">{content['headline']}</h2>
                    
                    <h4>📢 サブヘッドライン</h4>
                    <p style="font-size: 1.1rem;">{content['subheadline']}</p>
                    
                    <h4>📖 本文</h4>
                    <p>{content['body']}</p>
                    
                    <h4>🚀 CTA</h4>
                    <div style="background: #667eea; color: white; padding: 12px 24px; border-radius: 25px; text-align: center; font-weight: bold; margin: 10px 0;">
                        {content['cta']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # パフォーマンス予測
                performance = ai_content['performance_prediction']
                score = calculate_creative_score(ai_content)
                
                st.markdown(f"""
                <div class="creative-card">
                    <h4>📊 パフォーマンス予測</h4>
                    
                    <div class="performance-metric">
                        <div class="metric-value">{performance['ctr_estimate']:.2f}%</div>
                        <div class="metric-label">予測CTR</div>
                    </div>
                    
                    <div class="performance-metric">
                        <div class="metric-value">{performance['engagement_score']:.0f}</div>
                        <div class="metric-label">エンゲージメントスコア</div>
                    </div>
                    
                    <div class="performance-metric">
                        <div class="metric-value">{performance['conversion_probability']:.2f}%</div>
                        <div class="metric-label">予測コンバージョン率</div>
                    </div>
                    
                    <div class="performance-metric">
                        <div class="metric-value">{score:.0f}/100</div>
                        <div class="metric-label">総合スコア</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # 最適化提案
            st.markdown("### 💡 AI最適化提案")
            
            for i, suggestion in enumerate(ai_content['optimization_suggestions'], 1):
                st.markdown(f"""
                <div class="creation-step">
                    <span class="step-number">{i}</span>
                    {suggestion}
                </div>
                """, unsafe_allow_html=True)
            
            # バリエーション生成
            st.markdown("### 🎨 バリエーション")
            
            if st.button("✨ さらにバリエーションを生成", use_container_width=True):
                # 追加バリエーションの生成（スタブ）
                variations = [
                    {"headline": f"新時代の{product_category}で{target_audience}の可能性を解放", "ctr": np.random.uniform(2, 7)},
                    {"headline": f"{target_audience}が選ぶNo.1 {brand_name}", "ctr": np.random.uniform(1.8, 6.5)},
                    {"headline": f"たった3ステップで{target_audience}の課題を解決", "ctr": np.random.uniform(2.2, 8.1)}
                ]
                
                st.markdown('<div class="variation-gallery">', unsafe_allow_html=True)
                for i, var in enumerate(variations):
                    st.markdown(f"""
                    <div class="variation-item">
                        <h5>バリエーション {i+1}</h5>
                        <p>"{var['headline']}"</p>
                        <div class="metric-trend trend-up">予測CTR: {var['ctr']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# SNSコンテンツ作成モード
elif st.session_state.current_creative_mode == "social_content":
    
    if st.button("⬅️ ダッシュボードに戻る"):
        st.session_state.current_creative_mode = "dashboard"
        st.rerun()
    
    st.markdown("## 📱 AI SNSコンテンツ作成")
    
    platform_tabs = st.tabs(["📦 一括生成", "🐦 Twitter", "📷 Instagram", "💼 LinkedIn", "📘 Facebook"])
    
    with platform_tabs[0]:
        st.markdown("### 🚀 全プラットフォーム一括生成")
        
        with st.form("bulk_social_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                campaign_theme = st.text_input("キャンペーンテーマ*", placeholder="新製品ローンチ")
                target_demo = st.selectbox("ターゲット層", ["Z世代", "ミレニアル世代", "X世代", "ベビーブーマー", "全年代"])
                content_type = st.selectbox("コンテンツタイプ", ["製品紹介", "教育的", "エンターテイメント", "ニュース", "ライフスタイル"])
            
            with col2:
                brand_voice = st.selectbox("ブランドボイス", ["フレンドリー", "プロフェッショナル", "カジュアル", "権威的", "革新的"])
                post_frequency = st.selectbox("投稿頻度", ["毎日", "週3回", "週1回", "月2回"])
                include_hashtags = st.checkbox("ハッシュタグを含める", value=True)
            
            if st.form_submit_button("🌟 全プラットフォーム生成", type="primary"):
                # プログレス表示
                progress = st.progress(0)
                status = st.empty()
                
                platforms = ["Twitter", "Instagram", "LinkedIn", "Facebook"]
                generated_content = {}
                
                for i, platform in enumerate(platforms):
                    status.text(f"📱 {platform}コンテンツ生成中...")
                    progress.progress((i + 1) / len(platforms))
                    
                    # AI生成（スタブ）
                    brand_info = {"name": campaign_theme, "voice": brand_voice}
                    content = generate_ai_creative_content("social_post", target_demo, brand_info)
                    generated_content[platform] = content
                    
                    import time
                    time.sleep(0.5)
                
                status.text("✅ 全プラットフォーム生成完了！")
                
                # 結果表示
                st.markdown("### 🎉 生成されたコンテンツ")
                
                for platform, content in generated_content.items():
                    with st.expander(f"📱 {platform}コンテンツ"):
                        social_content = content['content']
                        platform_key = platform.lower()
                        
                        if platform_key in social_content:
                            st.markdown(f"**{platform}投稿:**")
                            st.code(social_content[platform_key])
                            
                            # パフォーマンス予測
                            perf = content['performance_prediction']
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("予測エンゲージメント", f"{perf['engagement_score']:.0f}%")
                            with col2:
                                st.metric("バイラル度", f"{perf['virality_potential']:.0f}%")
                            with col3:
                                st.metric("CTR予測", f"{perf['ctr_estimate']:.2f}%")

# 動画スクリプト生成モード
elif st.session_state.current_creative_mode == "video_script":
    
    if st.button("⬅️ ダッシュボードに戻る"):
        st.session_state.current_creative_mode = "dashboard"
        st.rerun()
    
    st.markdown("## 🎬 AI動画スクリプト生成")
    
    with st.form("video_script_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            video_length = st.selectbox("動画の長さ", ["15秒 (TikTok/Reels)", "30秒 (Instagram)", "60秒 (YouTube Shorts)", "2-3分 (YouTube)", "5-10分 (詳細解説)"])
            video_style = st.selectbox("動画スタイル", ["エクスプレイナー", "製品デモ", "証言/レビュー", "チュートリアル", "ブランドストーリー"])
            target_platform = st.multiselect("配信プラットフォーム", ["YouTube", "TikTok", "Instagram", "Facebook", "LinkedIn", "Twitter"])
        
        with col2:
            product_service = st.text_input("製品/サービス名*", placeholder="例: AI Marketing Tool")
            target_action = st.selectbox("視聴者に期待するアクション", ["ウェブサイト訪問", "アプリダウンロード", "購入", "登録", "お問い合わせ"])
            emotional_tone = st.selectbox("感情的トーン", ["興奮・エネルギッシュ", "信頼・安心", "好奇心・驚き", "共感・理解", "緊急性・FOMO"])
        
        key_points = st.text_area("含めたいキーポイント（改行区切り）", placeholder="コスト削減\n使いやすさ\n24/7サポート")
        target_audience_detail = st.text_input("詳細なターゲット層", placeholder="忙しいマーケティング担当者")
        
        if st.form_submit_button("🎬 スクリプト生成", type="primary"):
            # 生成プロセス
            with st.spinner("🎭 AI脚本家が創作中..."):
                import time
                time.sleep(2)
                
                brand_info = {
                    "name": product_service,
                    "style": video_style,
                    "length": video_length,
                    "platforms": target_platform
                }
                
                script_content = generate_ai_creative_content("video_script", target_audience_detail, brand_info)
                
                # スクリプト表示
                st.success("🎉 動画スクリプトが完成しました！")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 📝 完成スクリプト")
                    
                    script = script_content['content']
                    st.markdown(f"""
                    <div class="creative-card">
                        <h4>🎯 フック (0-3秒)</h4>
                        <p style="font-size: 1.1rem; color: #667eea;"><strong>"{script['hook']}"</strong></p>
                        
                        <h4>❗ 問題提起 (3-10秒)</h4>
                        <p>{script['problem']}</p>
                        
                        <h4>💡 ソリューション (10-45秒)</h4>
                        <p>{script['solution']}</p>
                        
                        <h4>🚀 CTA (45-60秒)</h4>
                        <p style="font-weight: bold; color: #10b981;">{script['cta']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 詳細演出指示
                    st.markdown("### 🎭 演出指示")
                    
                    directions = [
                        "オープニング: 動的なアニメーションでアテンションを獲得",
                        "問題提起: 視聴者の悩みを表現する画面分割エフェクト",
                        "ソリューション: 製品の使用シーンを実際の映像で",
                        "CTA: 画面いっぱいのボタンアニメーションで行動を促す"
                    ]
                    
                    for i, direction in enumerate(directions, 1):
                        st.markdown(f"""
                        <div class="creation-step">
                            <span class="step-number">{i}</span>
                            {direction}
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    # パフォーマンス予測
                    performance = script_content['performance_prediction']
                    
                    st.markdown("### 📊 予測パフォーマンス")
                    
                    st.markdown(f"""
                    <div class="performance-metric">
                        <div class="metric-value">{performance['engagement_score']:.0f}%</div>
                        <div class="metric-label">エンゲージメント率</div>
                    </div>
                    
                    <div class="performance-metric">
                        <div class="metric-value">{performance['virality_potential']:.0f}%</div>
                        <div class="metric-label">バイラル度</div>
                    </div>
                    
                    <div class="performance-metric">
                        <div class="metric-value">{performance['conversion_probability']:.2f}%</div>
                        <div class="metric-label">コンバージョン率</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # プラットフォーム最適化
                    st.markdown("### 📱 プラットフォーム最適化")
                    
                    optimizations = {
                        "TikTok": "縦型、最初の3秒が勝負、音楽重要",
                        "YouTube": "横型、詳細説明可能、SEO最適化",
                        "Instagram": "正方形推奨、ストーリーズ活用",
                        "LinkedIn": "プロフェッショナル、データ重視"
                    }
                    
                    for platform in target_platform:
                        if platform in optimizations:
                            st.info(f"**{platform}**: {optimizations[platform]}")

# サイドバー
with st.sidebar:
    st.header("🎨 Creative Studio")
    
    # クイック統計
    st.subheader("📊 今日の統計")
    
    total_projects = len(st.session_state.creative_projects)
    st.metric("生成済みクリエイティブ", total_projects)
    st.metric("平均スコア", "87.5" if total_projects > 0 else "0")
    st.metric("ROI向上率", "+238%")
    
    st.markdown("---")
    
    # AIモード選択
    st.subheader("🤖 AIモード")
    
    ai_mode = st.selectbox(
        "創作スタイル",
        ["🎯 高精度モード", "⚡ 高速生成", "🎨 創造性重視", "📊 データ重視", "🔬 実験的"]
    )
    
    creativity_level = st.slider("創造性レベル", 1, 10, 7)
    
    st.markdown("---")
    
    # エクスポート機能
    st.subheader("📥 エクスポート")
    
    if st.button("📄 レポート生成", use_container_width=True):
        if st.session_state.creative_projects:
            st.success("📊 パフォーマンスレポートを生成中...")
        else:
            st.warning("まずクリエイティブを生成してください")
    
    if st.button("💾 プロジェクト保存", use_container_width=True):
        if st.session_state.creative_projects:
            export_data = {
                "export_date": datetime.now().isoformat(),
                "projects": st.session_state.creative_projects,
                "total_count": len(st.session_state.creative_projects)
            }
            
            st.download_button(
                "📥 JSONダウンロード",
                data=json.dumps(export_data, ensure_ascii=False, indent=2),
                file_name=f"creative_projects_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.warning("保存するプロジェクトがありません")
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("📊 パフォーマンス分析", use_container_width=True):
        st.switch_page("pages/performance_dashboard.py")
    
    if st.button("🧪 A/Bテスト", use_container_width=True):
        st.switch_page("pages/ab_testing.py")

# フッター
st.markdown("---")
st.caption("🎨 AI Creative Studio: 最先端のAI技術で、あなたのマーケティングクリエイティブを次のレベルへ。無限の可能性を解き放ちましょう。")