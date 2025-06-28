#!/usr/bin/env python3
"""
価格戦略コンサルティングページ
個人開発・SaaSのための価格設定戦略 完全ガイド
PSM分析、LTV/CAC計算機、価格シミュレーター等を提供
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import asyncio
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# AI価格戦略分析関数
async def analyze_pricing_strategy_with_ai(
    product_data: Dict, 
    market_data: Dict, 
    financial_data: Dict
) -> Dict[str, Any]:
    """AI駆動の価格戦略分析"""
    USE_MOCK_AI = os.getenv('USE_MOCK_AI', 'false').lower() == 'true'
    
    if USE_MOCK_AI:
        return analyze_pricing_strategy_mock(product_data, market_data, financial_data)
    
    try:
        from config.ai_client import ai_client
        from config.ai_models import TaskType
        
        analysis_prompt = f"""
        製品の価格戦略を分析してください：

        製品情報:
        - 製品タイプ: {product_data.get('type', 'unknown')}
        - 機能数: {product_data.get('features', 0)}
        - 開発期間: {product_data.get('development_months', 0)}ヶ月
        - チーム規模: {product_data.get('team_size', 1)}人

        市場データ:
        - ターゲット市場規模: {market_data.get('market_size', 0)}
        - 競合製品数: {market_data.get('competitors', 0)}
        - 平均価格帯: {market_data.get('avg_price', 0)}円

        財務データ:
        - 開発コスト: {financial_data.get('development_cost', 0)}円
        - 月間固定費: {financial_data.get('monthly_cost', 0)}円
        - 目標利益率: {financial_data.get('target_margin', 30)}%

        以下の形式でJSON回答してください：
        {{
            "recommended_pricing_strategy": {{
                "strategy_type": "価格戦略名（penetration/skimming/competitive/value_based）",
                "base_price": 9800,
                "price_tiers": [
                    {{"name": "Basic", "price": 1980, "features": ["機能A"]}},
                    {{"name": "Pro", "price": 4980, "features": ["機能A", "機能B"]}},
                    {{"name": "Enterprise", "price": 9800, "features": ["全機能"]}}
                ],
                "reasoning": "戦略選択の理由"
            }},
            "market_positioning": {{
                "competitive_advantage": ["差別化要因1", "差別化要因2"],
                "target_segments": ["セグメント1", "セグメント2"],
                "value_proposition": "価値提案"
            }},
            "pricing_optimization": {{
                "psychological_pricing": true,
                "bundling_opportunities": ["バンドル案1", "バンドル案2"],
                "discount_strategy": "適切な割引戦略",
                "freemium_viability": 0.8
            }},
            "financial_projections": {{
                "break_even_units": 100,
                "monthly_revenue_potential": 500000,
                "ltv_estimate": 50000,
                "payback_period_months": 6
            }},
            "recommendations": [
                "具体的な推奨事項1",
                "具体的な推奨事項2",
                "具体的な推奨事項3"
            ],
            "confidence_score": 0.85
        }}
        """
        
        response = await ai_client.chat_completion(
            messages=[{"role": "user", "content": analysis_prompt}],
            task_type=TaskType.DATA_ANALYSIS
        )
        
        import json
        try:
            result = json.loads(response['content'])
            result['ai_generated'] = True
            result['timestamp'] = datetime.now().isoformat()
            return result
        except json.JSONDecodeError:
            return analyze_pricing_strategy_mock(product_data, market_data, financial_data)
            
    except Exception as e:
        print(f"AI pricing analysis error: {e}")
        return analyze_pricing_strategy_mock(product_data, market_data, financial_data)

def analyze_pricing_strategy_mock(
    product_data: Dict, 
    market_data: Dict, 
    financial_data: Dict
) -> Dict[str, Any]:
    """価格戦略分析のモック版"""
    
    # 基本的な計算
    dev_cost = financial_data.get('development_cost', 1000000)
    monthly_cost = financial_data.get('monthly_cost', 100000)
    target_margin = financial_data.get('target_margin', 30) / 100
    market_size = market_data.get('market_size', 10000)
    avg_price = market_data.get('avg_price', 5000)
    
    # 戦略タイプの決定
    if avg_price > 10000:
        strategy_type = "penetration"  # 市場浸透価格
        base_price = int(avg_price * 0.7)
    elif market_size > 50000:
        strategy_type = "competitive"  # 競争価格
        base_price = int(avg_price * 0.9)
    else:
        strategy_type = "value_based"  # 価値ベース価格
        base_price = int(avg_price * 1.2)
    
    # 価格ティアの生成
    price_tiers = [
        {
            "name": "Starter",
            "price": int(base_price * 0.4),
            "features": ["基本機能", "標準サポート"]
        },
        {
            "name": "Professional", 
            "price": base_price,
            "features": ["全機能", "優先サポート", "詳細分析"]
        },
        {
            "name": "Enterprise",
            "price": int(base_price * 2),
            "features": ["全機能", "専任サポート", "カスタマイズ", "API"]
        }
    ]
    
    # 収益性計算
    estimated_conversion = 0.02 if strategy_type == "penetration" else 0.015
    monthly_customers = int(market_size * estimated_conversion)
    monthly_revenue = monthly_customers * base_price
    break_even_units = int((dev_cost / 12 + monthly_cost) / (base_price * target_margin))
    
    return {
        "recommended_pricing_strategy": {
            "strategy_type": strategy_type,
            "base_price": base_price,
            "price_tiers": price_tiers,
            "reasoning": f"{strategy_type}戦略により市場シェア獲得と収益性のバランスを図る"
        },
        "market_positioning": {
            "competitive_advantage": ["コストパフォーマンス", "ユーザビリティ", "カスタマーサポート"],
            "target_segments": ["スタートアップ", "中小企業", "個人事業主"],
            "value_proposition": "手軽に始められる高機能ソリューション"
        },
        "pricing_optimization": {
            "psychological_pricing": True,
            "bundling_opportunities": ["年間プラン（20%割引）", "複数機能パック"],
            "discount_strategy": "新規顧客30日間無料トライアル",
            "freemium_viability": 0.7
        },
        "financial_projections": {
            "break_even_units": break_even_units,
            "monthly_revenue_potential": monthly_revenue,
            "ltv_estimate": int(base_price * 8),  # 平均8ヶ月利用想定
            "payback_period_months": max(3, int(dev_cost / monthly_revenue)) if monthly_revenue > 0 else 12
        },
        "recommendations": [
            f"市場平均より{'低い' if strategy_type == 'penetration' else '競争力のある'}価格設定で参入",
            "多層価格体系でさまざまな顧客ニーズに対応",
            "無料トライアルで導入ハードルを下げる",
            "年間契約による割引で顧客ロイヤルティ向上",
            "定期的な価格見直しで市場変化に対応"
        ],
        "confidence_score": 0.75,
        "ai_generated": False,
        "timestamp": datetime.now().isoformat()
    }

async def optimize_price_with_ai(
    current_price: float,
    performance_data: Dict,
    goals: Dict
) -> Dict[str, Any]:
    """AI駆動の価格最適化"""
    USE_MOCK_AI = os.getenv('USE_MOCK_AI', 'false').lower() == 'true'
    
    if USE_MOCK_AI:
        return optimize_price_mock(current_price, performance_data, goals)
    
    try:
        from config.ai_client import ai_client
        from config.ai_models import TaskType
        
        optimization_prompt = f"""
        価格最適化の提案をしてください：

        現在の価格: {current_price}円
        
        パフォーマンスデータ:
        - 月間新規顧客: {performance_data.get('monthly_new_customers', 0)}
        - 解約率: {performance_data.get('churn_rate', 0.05)*100}%
        - 顧客満足度: {performance_data.get('satisfaction_score', 3.5)}/5
        - コンバージョン率: {performance_data.get('conversion_rate', 0.02)*100}%

        目標:
        - 収益目標: {goals.get('revenue_target', 1000000)}円/月
        - 顧客数目標: {goals.get('customer_target', 500)}人
        - 利益率目標: {goals.get('margin_target', 30)}%

        以下の形式でJSON回答してください：
        {{
            "optimized_prices": {{
                "recommended_price": 8800,
                "price_range": {{"min": 7800, "max": 9800}},
                "adjustment_percentage": 10.5,
                "reasoning": "最適化の根拠"
            }},
            "ab_test_suggestions": [
                {{"price": 8500, "expected_conversion": 0.025, "risk_level": "low"}},
                {{"price": 9200, "expected_conversion": 0.018, "risk_level": "medium"}}
            ],
            "timing_strategy": {{
                "implementation_timeline": "段階的実装スケジュール",
                "grandfathering_strategy": "既存顧客への対応",
                "announcement_timing": "発表タイミング"
            }},
            "expected_impact": {{
                "revenue_change": 15.2,
                "customer_change": -5.0,
                "conversion_change": 8.5
            }},
            "risks_and_mitigation": [
                "リスク要因と対策"
            ],
            "monitoring_metrics": [
                "監視すべき指標"
            ]
        }}
        """
        
        response = await ai_client.chat_completion(
            messages=[{"role": "user", "content": optimization_prompt}],
            task_type=TaskType.DATA_ANALYSIS
        )
        
        import json
        try:
            result = json.loads(response['content'])
            result['ai_generated'] = True
            return result
        except json.JSONDecodeError:
            return optimize_price_mock(current_price, performance_data, goals)
            
    except Exception as e:
        print(f"AI price optimization error: {e}")
        return optimize_price_mock(current_price, performance_data, goals)

def optimize_price_mock(current_price: float, performance_data: Dict, goals: Dict) -> Dict[str, Any]:
    """価格最適化のモック版"""
    
    conversion_rate = performance_data.get('conversion_rate', 0.02)
    satisfaction = performance_data.get('satisfaction_score', 3.5)
    churn_rate = performance_data.get('churn_rate', 0.05)
    
    # 最適化ロジック
    price_elasticity = -0.5  # 価格弾力性仮定
    
    # 顧客満足度に基づく価格調整余地
    if satisfaction > 4.0:
        price_multiplier = 1.1  # 10%値上げ余地
    elif satisfaction < 3.0:
        price_multiplier = 0.9  # 10%値下げ推奨
    else:
        price_multiplier = 1.0
    
    # 解約率に基づく調整
    if churn_rate > 0.1:
        price_multiplier *= 0.95  # 価格競争力向上
    
    recommended_price = int(current_price * price_multiplier)
    adjustment_percentage = (recommended_price / current_price - 1) * 100
    
    return {
        "optimized_prices": {
            "recommended_price": recommended_price,
            "price_range": {
                "min": int(recommended_price * 0.9),
                "max": int(recommended_price * 1.1)
            },
            "adjustment_percentage": adjustment_percentage,
            "reasoning": f"顧客満足度{satisfaction:.1f}と解約率{churn_rate*100:.1f}%を考慮した最適化"
        },
        "ab_test_suggestions": [
            {
                "price": int(current_price * 0.95),
                "expected_conversion": conversion_rate * 1.1,
                "risk_level": "low"
            },
            {
                "price": int(current_price * 1.05),
                "expected_conversion": conversion_rate * 0.95,
                "risk_level": "medium"
            }
        ],
        "timing_strategy": {
            "implementation_timeline": "3段階で4週間かけて実装",
            "grandfathering_strategy": "既存顧客は3ヶ月据え置き",
            "announcement_timing": "実装2週間前に事前告知"
        },
        "expected_impact": {
            "revenue_change": adjustment_percentage * 0.7,  # 価格弾力性考慮
            "customer_change": adjustment_percentage * price_elasticity,
            "conversion_change": -adjustment_percentage * 0.3
        },
        "risks_and_mitigation": [
            "既存顧客の離脱リスク → 段階的移行でソフトランディング",
            "競合他社の価格対応 → 差別化価値の強化",
            "市場の価格感度 → A/Bテストで慎重に検証"
        ],
        "monitoring_metrics": [
            "月間新規登録数",
            "解約率",
            "顧客満足度スコア",
            "価格に関する問い合わせ数",
            "競合比較サイトでの評価"
        ],
        "ai_generated": False
    }

# ページ設定
st.set_page_config(
    page_title="価格戦略コンサルティング - shigotoba.io",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .strategy-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid rgba(34, 197, 94, 0.2);
        transition: all 0.3s;
        height: 100%;
    }
    
    .strategy-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(34, 197, 94, 0.2);
        border-color: rgba(34, 197, 94, 0.4);
    }
    
    .pricing-header {
        background: linear-gradient(90deg, #22c55e, #16a34a);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
    
    .pricing-title {
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
    }
    
    .pricing-subtitle {
        color: #dcfce7;
        font-size: 1rem;
        margin: 5px 0 0 0;
    }
    
    .calculator-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin: 10px 0;
    }
    
    .result-highlight {
        background: rgba(34, 197, 94, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #22c55e;
        margin: 10px 0;
    }
    
    .warning-box {
        background: rgba(245, 158, 11, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# プロジェクトコンテキスト表示
current_project = None
if hasattr(st.session_state, 'current_project') and st.session_state.current_project:
    if 'projects' in st.session_state:
        current_project = st.session_state.projects.get(st.session_state.current_project)

if current_project:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%); 
                padding: 15px; border-radius: 10px; margin: 10px 0 20px 0;
                border: 1px solid rgba(34, 197, 94, 0.3);">
        <p style="margin: 0; color: white; font-weight: bold;">🎯 プロジェクト連動モード</p>
        <p style="margin: 5px 0 0 0; color: #dcfce7; font-size: 0.9rem;">
            {current_project['name']} の価格戦略を最適化します
        </p>
    </div>
    """, unsafe_allow_html=True)

# ホームに戻るボタン
if st.button("🏠 ホームに戻る", type="secondary"):
    st.switch_page("app.py")

# タブによる機能分割
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 価格戦略ガイド", 
    "📊 PSM分析", 
    "💹 LTV/CAC計算機", 
    "🎯 価格シミュレーター", 
    "📈 成長戦略"
])

# タブ1: 価格戦略ガイド
with tab1:
    st.markdown("## 🎯 価格設定の基本戦略")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="strategy-card">
            <h3>🔥 価値ベース価格設定</h3>
            <p><strong>最も推奨される手法</strong></p>
            <ul>
                <li>顧客が感じる価値を基準</li>
                <li>競合より高価格でも正当化可能</li>
                <li>差別化要素の明確化が重要</li>
                <li>利益率最大化を実現</li>
            </ul>
            <div class="result-highlight">
                <strong>適用例:</strong> 独自機能を持つSaaS、ニッチ市場向けサービス
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="strategy-card">
            <h3>⚖️ 競合ベース価格設定</h3>
            <p><strong>市場参入時の安全策</strong></p>
            <ul>
                <li>競合の価格を基準に設定</li>
                <li>市場の受容価格を把握</li>
                <li>差別化が困難な場合に有効</li>
                <li>価格競争のリスク有り</li>
            </ul>
            <div class="warning-box">
                <strong>注意:</strong> 利益率圧迫の可能性
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="strategy-card">
            <h3>📊 コストプラス価格設定</h3>
            <p><strong>シンプルだが制限的</strong></p>
            <ul>
                <li>コスト + 利益マージン</li>
                <li>計算が簡単で分かりやすい</li>
                <li>顧客価値を無視するリスク</li>
                <li>機会損失の可能性</li>
            </ul>
            <div class="warning-box">
                <strong>推奨度:</strong> 低（補助的使用のみ）
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SaaS価格モデル
    st.markdown("## 🏢 SaaS価格モデル比較")
    
    pricing_models = {
        'モデル': ['ユーザー単価', '使用量ベース', '階層プラン', 'フリーミアム', '一括購入'],
        '適用場面': [
            'チーム利用、管理者機能重要',
            'API利用、データ処理量に依存',
            '機能差別化、様々な顧客層',
            'ユーザー獲得重視、ネットワーク効果',
            '継続課金を避けたい顧客向け'
        ],
        'メリット': [
            '予測しやすい収益、拡張性',
            '使用量に応じた公平な価格',
            '顧客ニーズに応じた選択肢',
            '大量ユーザー獲得、口コミ効果',
            '初期収益確保、顧客安心感'
        ],
        'デメリット': [
            'ユーザー数制限による成長阻害',
            '収益予測困難、管理複雑',
            'プラン設計の複雑さ',
            '無料ユーザーのコスト負担',
            '継続収益なし、サポートコスト'
        ]
    }
    
    df_models = pd.DataFrame(pricing_models)
    st.dataframe(df_models, use_container_width=True)
    
    st.markdown("---")
    
    # 製品ライフサイクル別戦略
    st.markdown("## 📈 製品ライフサイクル別価格戦略")
    
    lifecycle_cols = st.columns(4)
    
    with lifecycle_cols[0]:
        st.markdown("""
        <div class="strategy-card">
            <h4>🚀 導入期</h4>
            <p><strong>市場浸透戦略</strong></p>
            <ul>
                <li>低価格でユーザー獲得</li>
                <li>フリーミアム導入</li>
                <li>早期割引提供</li>
                <li>市場シェア重視</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with lifecycle_cols[1]:
        st.markdown("""
        <div class="strategy-card">
            <h4>📈 成長期</h4>
            <p><strong>価値最適化</strong></p>
            <ul>
                <li>段階的値上げ</li>
                <li>機能別価格設定</li>
                <li>顧客セグメント価格</li>
                <li>価値証明の強化</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with lifecycle_cols[2]:
        st.markdown("""
        <div class="strategy-card">
            <h4>🏆 成熟期</h4>
            <p><strong>利益最大化</strong></p>
            <ul>
                <li>プレミアム価格</li>
                <li>バンドル戦略</li>
                <li>アップセル強化</li>
                <li>ロイヤルティ重視</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with lifecycle_cols[3]:
        st.markdown("""
        <div class="strategy-card">
            <h4>📉 衰退期</h4>
            <p><strong>撤退・転換戦略</strong></p>
            <ul>
                <li>在庫処分価格</li>
                <li>サブスク→買切変更</li>
                <li>新製品への誘導</li>
                <li>コスト最小化</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# タブ2: PSM分析
with tab2:
    st.markdown("## 📊 PSM（Price Sensitivity Meter）分析")
    st.markdown("**Van Westendorp法による価格感度分析 - 最適価格帯を科学的に決定**")
    
    # PSM分析の説明
    with st.expander("🔍 PSM分析とは？"):
        st.markdown("""
        PSM分析は4つの質問で構成される価格調査手法です：
        
        1. **安すぎる価格**: この価格では品質に不安を感じる
        2. **安い価格**: お得だと感じる価格
        3. **高い価格**: 少し高いと感じるが購入を検討する価格
        4. **高すぎる価格**: 高すぎて購入しない価格
        
        これらの累積グラフの交点から最適価格帯を導出します。
        """)
    
    # サンプルデータ入力
    st.markdown("### 📝 調査データ入力")
    
    sample_data = st.checkbox("サンプルデータを使用（SaaS月額料金の例）", value=True)
    
    if sample_data:
        # SaaSの月額料金サンプル（50人の回答想定）
        np.random.seed(42)
        too_cheap = np.random.normal(500, 150, 50).astype(int)
        cheap = np.random.normal(800, 200, 50).astype(int)
        expensive = np.random.normal(2000, 300, 50).astype(int)
        too_expensive = np.random.normal(3500, 500, 50).astype(int)
        
        st.info("💡 SaaS月額料金の調査例（50人の回答）を表示中")
    else:
        st.markdown("**カスタムデータ入力**（カンマ区切りで価格を入力）:")
        too_cheap_input = st.text_area("安すぎる価格", "500,400,600,550...")
        cheap_input = st.text_area("安い価格", "800,750,900,850...")
        expensive_input = st.text_area("高い価格", "2000,1800,2200,1900...")
        too_expensive_input = st.text_area("高すぎる価格", "3500,3000,4000,3200...")
        
        try:
            too_cheap = [int(x.strip()) for x in too_cheap_input.split(',') if x.strip()]
            cheap = [int(x.strip()) for x in cheap_input.split(',') if x.strip()]
            expensive = [int(x.strip()) for x in expensive_input.split(',') if x.strip()]
            too_expensive = [int(x.strip()) for x in too_expensive_input.split(',') if x.strip()]
        except:
            st.error("数値を正しく入力してください")
            too_cheap = cheap = expensive = too_expensive = []
    
    if len(too_cheap) > 0:
        # PSM分析計算
        all_prices = sorted(set(too_cheap + cheap + expensive + too_expensive))
        min_price, max_price = min(all_prices), max(all_prices)
        price_range = np.linspace(min_price, max_price, 100)
        
        # 累積パーセンテージ計算
        too_cheap_cum = [sum(1 for x in too_cheap if x >= p) / len(too_cheap) * 100 for p in price_range]
        cheap_cum = [sum(1 for x in cheap if x >= p) / len(cheap) * 100 for p in price_range]
        expensive_cum = [sum(1 for x in expensive if x <= p) / len(expensive) * 100 for p in price_range]
        too_expensive_cum = [sum(1 for x in too_expensive if x <= p) / len(too_expensive) * 100 for p in price_range]
        
        # グラフ作成
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=price_range, y=too_cheap_cum,
            name='安すぎる', line=dict(color='red', dash='dash'),
            hovertemplate='価格: ¥%{x:,.0f}<br>%{y:.1f}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=price_range, y=cheap_cum,
            name='安い', line=dict(color='green'),
            hovertemplate='価格: ¥%{x:,.0f}<br>%{y:.1f}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=price_range, y=expensive_cum,
            name='高い', line=dict(color='orange'),
            hovertemplate='価格: ¥%{x:,.0f}<br>%{y:.1f}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=price_range, y=too_expensive_cum,
            name='高すぎる', line=dict(color='red'),
            hovertemplate='価格: ¥%{x:,.0f}<br>%{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='PSM分析結果 - 価格感度曲線',
            xaxis_title='価格 (¥)',
            yaxis_title='累積パーセンテージ (%)',
            template='plotly_dark',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 最適価格帯の計算（簡単な交点計算）
        acceptable_range_low = np.interp(50, cheap_cum[::-1], price_range[::-1])
        acceptable_range_high = np.interp(50, expensive_cum, price_range)
        optimal_price = (acceptable_range_low + acceptable_range_high) / 2
        
        # 結果表示
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="result-highlight">
                <h4>💰 最適価格</h4>
                <h2>¥{optimal_price:,.0f}</h2>
                <p>最も受け入れられやすい価格</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="result-highlight">
                <h4>📉 受容価格帯（下限）</h4>
                <h2>¥{acceptable_range_low:,.0f}</h2>
                <p>これ以下は安すぎると感じられる</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="result-highlight">
                <h4>📈 受容価格帯（上限）</h4>
                <h2>¥{acceptable_range_high:,.0f}</h2>
                <p>これ以上は高すぎると感じられる</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 価格戦略提案
        st.markdown("### 🎯 価格戦略提案")
        
        strategy_cols = st.columns(2)
        
        with strategy_cols[0]:
            st.markdown(f"""
            **💡 推奨価格戦略:**
            
            - **市場導入価格**: ¥{acceptable_range_low * 0.9:,.0f} (下限の90%)
            - **標準価格**: ¥{optimal_price:,.0f} (最適価格)
            - **プレミアム価格**: ¥{acceptable_range_high * 0.95:,.0f} (上限の95%)
            """)
        
        with strategy_cols[1]:
            penetration_rate = (acceptable_range_high - acceptable_range_low) / acceptable_range_high * 100
            st.markdown(f"""
            **📊 市場分析:**
            
            - **価格許容度**: {penetration_rate:.1f}%
            - **価格弾力性**: {'高' if penetration_rate > 50 else '中' if penetration_rate > 30 else '低'}
            - **推奨戦略**: {'段階的値上げ' if penetration_rate > 40 else 'プレミアム戦略'}
            """)
        
        # AI価格戦略分析セクション
        st.markdown("---")
        st.markdown("### 🤖 AI価格戦略分析")
        
        # AI分析実行ボタン
        if st.button("🔍 AI戦略分析を実行", key="ai_pricing_analysis"):
            # 入力データを整理
            product_data = {
                'type': 'SaaS',  # デフォルト
                'features': 10,  # 仮想値
                'development_months': 6,
                'team_size': 3
            }
            
            market_data = {
                'market_size': 100000,  # 仮想値
                'competitors': 15,
                'avg_price': optimal_price
            }
            
            financial_data = {
                'development_cost': 2000000,  # 仮想値
                'monthly_cost': 200000,
                'target_margin': 40
            }
            
            with st.spinner("AI分析を実行中..."):
                try:
                    # 非同期関数を同期実行
                    loop = None
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    if loop.is_running():
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run, 
                                analyze_pricing_strategy_with_ai(product_data, market_data, financial_data)
                            )
                            ai_analysis = future.result(timeout=15)
                    else:
                        ai_analysis = loop.run_until_complete(
                            analyze_pricing_strategy_with_ai(product_data, market_data, financial_data)
                        )
                    
                    # AI分析結果を表示
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 💡 AI推奨価格戦略")
                        strategy = ai_analysis.get('recommended_pricing_strategy', {})
                        
                        st.markdown(f"""
                        <div class="result-highlight">
                            <strong>戦略タイプ:</strong> {strategy.get('strategy_type', 'N/A')}<br>
                            <strong>推奨価格:</strong> ¥{strategy.get('base_price', 0):,}<br>
                            <strong>理由:</strong> {strategy.get('reasoning', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 価格ティア表示
                        st.markdown("##### 📊 推奨価格ティア")
                        price_tiers = strategy.get('price_tiers', [])
                        for tier in price_tiers:
                            st.markdown(f"""
                            **{tier.get('name', 'N/A')}**: ¥{tier.get('price', 0):,}
                            - {', '.join(tier.get('features', []))}
                            """)
                    
                    with col2:
                        st.markdown("#### 🎯 市場ポジショニング")
                        positioning = ai_analysis.get('market_positioning', {})
                        
                        st.markdown("**競争優位性:**")
                        for advantage in positioning.get('competitive_advantage', []):
                            st.markdown(f"• {advantage}")
                        
                        st.markdown("**ターゲットセグメント:**")
                        for segment in positioning.get('target_segments', []):
                            st.markdown(f"• {segment}")
                        
                        st.markdown(f"**価値提案:** {positioning.get('value_proposition', 'N/A')}")
                    
                    # 財務予測
                    st.markdown("#### 💹 財務予測")
                    projections = ai_analysis.get('financial_projections', {})
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("損益分岐点", f"{projections.get('break_even_units', 0)}件")
                    with col2:
                        st.metric("月間売上予測", f"¥{projections.get('monthly_revenue_potential', 0):,}")
                    with col3:
                        st.metric("LTV予測", f"¥{projections.get('ltv_estimate', 0):,}")
                    with col4:
                        st.metric("回収期間", f"{projections.get('payback_period_months', 0)}ヶ月")
                    
                    # 推奨事項
                    st.markdown("#### ✨ AI推奨事項")
                    recommendations = ai_analysis.get('recommendations', [])
                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"{i}. {rec}")
                    
                    # 最適化機会
                    optimization = ai_analysis.get('pricing_optimization', {})
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**バンドリング機会:**")
                        for opportunity in optimization.get('bundling_opportunities', []):
                            st.markdown(f"• {opportunity}")
                    
                    with col2:
                        freemium_score = optimization.get('freemium_viability', 0)
                        st.markdown(f"**フリーミアム適性:** {freemium_score*100:.0f}%")
                        st.progress(freemium_score)
                        st.markdown(f"**割引戦略:** {optimization.get('discount_strategy', 'N/A')}")
                    
                    # 信頼度スコア
                    confidence = ai_analysis.get('confidence_score', 0.75)
                    ai_generated = ai_analysis.get('ai_generated', False)
                    
                    st.markdown(f"""
                    <div style="text-align: center; margin: 20px 0; padding: 15px; background: rgba(34, 197, 94, 0.1); border-radius: 8px;">
                        <div style="color: #22c55e;">
                            {'🤖' if ai_generated else '📊'} 
                            {'AI分析' if ai_generated else 'ルールベース分析'} | 
                            信頼度: {confidence*100:.1f}%
                        </div>
                        <div style="color: #64748b; font-size: 0.8rem;">
                            分析時刻: {ai_analysis.get('timestamp', datetime.now().isoformat())[:19]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"AI分析でエラーが発生しました: {str(e)}")
                    st.info("手動でデータを入力して基本的な価格戦略を検討してください。")

# タブ3: LTV/CAC計算機
with tab3:
    st.markdown("## 💹 LTV/CAC計算機")
    st.markdown("**顧客生涯価値と顧客獲得コストの分析 - SaaSビジネスの核心指標**")
    
    # 基本メトリクス入力
    st.markdown("### 📝 基本メトリクス入力")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💰 収益関連**")
        monthly_revenue = st.number_input("月間売上単価 (¥)", value=5000, step=100)
        gross_margin = st.slider("グロスマージン率 (%)", 0, 100, 80)
        
        st.markdown("**📈 成長関連**")
        monthly_churn_rate = st.slider("月次解約率 (%)", 0.0, 20.0, 3.0, 0.1)
        upsell_rate = st.slider("アップセル率 (%/月)", 0.0, 10.0, 2.0, 0.1)
    
    with col2:
        st.markdown("**💸 コスト関連**")
        cac = st.number_input("顧客獲得コスト (CAC) ¥", value=15000, step=1000)
        support_cost = st.number_input("月間サポートコスト (¥)", value=500, step=50)
        
        st.markdown("**⏱️ 時間関連**")
        payback_period_target = st.slider("目標回収期間 (月)", 1, 24, 12)
    
    # 計算処理
    monthly_churn_decimal = monthly_churn_rate / 100
    annual_churn_rate = 1 - (1 - monthly_churn_decimal) ** 12
    customer_lifespan_months = 1 / monthly_churn_decimal if monthly_churn_decimal > 0 else float('inf')
    
    gross_monthly_revenue = monthly_revenue * (gross_margin / 100)
    net_monthly_revenue = gross_monthly_revenue - support_cost
    
    # LTV計算（複利効果考慮）
    if monthly_churn_decimal > 0:
        growth_factor = 1 + (upsell_rate / 100)
        ltv = net_monthly_revenue * growth_factor / monthly_churn_decimal
    else:
        ltv = float('inf')
    
    ltv_cac_ratio = ltv / cac if cac > 0 else float('inf')
    payback_period = cac / net_monthly_revenue if net_monthly_revenue > 0 else float('inf')
    
    # 結果表示
    st.markdown("### 📊 計算結果")
    
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric(
            "顧客生涯価値 (LTV)",
            f"¥{ltv:,.0f}" if ltv != float('inf') else "∞", 
            delta=None
        )
    
    with metric_cols[1]:
        color = "normal" if ltv_cac_ratio >= 3 else "inverse"
        st.metric(
            "LTV/CAC比率",
            f"{ltv_cac_ratio:.1f}" if ltv_cac_ratio != float('inf') else "∞",
            delta="健全" if ltv_cac_ratio >= 3 else "要改善"
        )
    
    with metric_cols[2]:
        color = "normal" if payback_period <= payback_period_target else "inverse"
        st.metric(
            "回収期間",
            f"{payback_period:.1f}ヶ月" if payback_period != float('inf') else "∞",
            delta="目標内" if payback_period <= payback_period_target else "目標超過"
        )
    
    with metric_cols[3]:
        st.metric(
            "顧客寿命",
            f"{customer_lifespan_months:.1f}ヶ月" if customer_lifespan_months != float('inf') else "∞",
            delta=None
        )
    
    # 健全性評価
    st.markdown("### 🏥 ビジネス健全性評価")
    
    health_cols = st.columns(3)
    
    with health_cols[0]:
        if ltv_cac_ratio >= 5:
            health_status = "🟢 優秀"
            health_message = "非常に健全なユニットエコノミクス"
        elif ltv_cac_ratio >= 3:
            health_status = "🟡 良好"
            health_message = "健全だが改善余地あり"
        else:
            health_status = "🔴 要改善"
            health_message = "ユニットエコノミクスに課題"
        
        st.markdown(f"""
        <div class="result-highlight">
            <h4>LTV/CAC評価</h4>
            <h3>{health_status}</h3>
            <p>{health_message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with health_cols[1]:
        if payback_period <= 6:
            payback_status = "🟢 優秀"
            payback_message = "迅速な投資回収"
        elif payback_period <= 12:
            payback_status = "🟡 良好"
            payback_message = "妥当な回収期間"
        else:
            payback_status = "🔴 要改善"
            payback_message = "回収期間が長すぎる"
        
        st.markdown(f"""
        <div class="result-highlight">
            <h4>回収期間評価</h4>
            <h3>{payback_status}</h3>
            <p>{payback_message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with health_cols[2]:
        if monthly_churn_rate <= 2:
            churn_status = "🟢 優秀"
            churn_message = "低い解約率"
        elif monthly_churn_rate <= 5:
            churn_status = "🟡 平均"
            churn_message = "業界平均レベル"
        else:
            churn_status = "🔴 要改善"
            churn_message = "解約率が高い"
        
        st.markdown(f"""
        <div class="result-highlight">
            <h4>解約率評価</h4>
            <h3>{churn_status}</h3>
            <p>{churn_message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 改善提案
    st.markdown("### 💡 改善提案")
    
    suggestions = []
    
    if ltv_cac_ratio < 3:
        suggestions.append("🎯 **LTV向上策**: 価格最適化、アップセル強化、解約率削減")
        suggestions.append("💰 **CAC削減策**: マーケティング効率化、紹介プログラム強化")
    
    if payback_period > 12:
        suggestions.append("⚡ **回収期間短縮**: 年間契約割引、初期費用見直し")
    
    if monthly_churn_rate > 5:
        suggestions.append("🤝 **解約率改善**: オンボーディング強化、カスタマーサクセス投資")
    
    if not suggestions:
        suggestions.append("🎉 **継続強化**: 現在の指標は健全です。更なる最適化を検討してください")
    
    for suggestion in suggestions:
        st.markdown(suggestion)
    
    # シナリオ分析
    st.markdown("---")
    st.markdown("### 🔮 シナリオ分析")
    
    scenario_cols = st.columns(3)
    
    scenarios = {
        "現状維持": {"churn_change": 0, "price_change": 0, "cac_change": 0},
        "価格10%アップ": {"churn_change": 1, "price_change": 10, "cac_change": 0},
        "解約率半減": {"churn_change": -50, "price_change": 0, "cac_change": 0}
    }
    
    for i, (scenario_name, changes) in enumerate(scenarios.items()):
        new_churn = max(0.1, monthly_churn_rate + changes["churn_change"])
        new_price = monthly_revenue * (1 + changes["price_change"] / 100)
        new_cac = cac * (1 + changes["cac_change"] / 100)
        
        new_monthly_churn_decimal = new_churn / 100
        new_gross_monthly_revenue = new_price * (gross_margin / 100)
        new_net_monthly_revenue = new_gross_monthly_revenue - support_cost
        
        if new_monthly_churn_decimal > 0:
            growth_factor = 1 + (upsell_rate / 100)
            new_ltv = new_net_monthly_revenue * growth_factor / new_monthly_churn_decimal
        else:
            new_ltv = float('inf')
        
        new_ltv_cac_ratio = new_ltv / new_cac if new_cac > 0 else float('inf')
        
        with scenario_cols[i]:
            st.markdown(f"""
            <div class="calculator-box">
                <h4>{scenario_name}</h4>
                <p><strong>LTV:</strong> ¥{new_ltv:,.0f}</p>
                <p><strong>LTV/CAC:</strong> {new_ltv_cac_ratio:.1f}</p>
                <p><strong>変化:</strong> {((new_ltv_cac_ratio - ltv_cac_ratio) / ltv_cac_ratio * 100):+.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

# タブ4: 価格シミュレーター
with tab4:
    st.markdown("## 🎯 価格シミュレーター")
    st.markdown("**異なる価格戦略の収益インパクトを予測**")
    
    # シミュレーション設定
    st.markdown("### ⚙️ シミュレーション設定")
    
    sim_cols = st.columns(2)
    
    with sim_cols[0]:
        st.markdown("**📊 市場前提条件**")
        total_addressable_market = st.number_input("総市場規模（TAM）", value=100000, step=10000)
        market_penetration = st.slider("市場浸透率 (%)", 0.1, 10.0, 2.0, 0.1)
        competition_factor = st.slider("競合影響度", 0.1, 2.0, 1.0, 0.1)
        
        st.markdown("**💼 ビジネス前提**")
        base_conversion_rate = st.slider("基準コンバージョン率 (%)", 1.0, 20.0, 5.0, 0.1)
        operational_cost_ratio = st.slider("運営コスト率 (%)", 10, 80, 40)
    
    with sim_cols[1]:
        st.markdown("**📈 価格戦略選択**")
        
        strategy_type = st.selectbox(
            "価格戦略",
            ["ペネトレーション（低価格浸透）", "スキミング（高価格戦略）", "競合追従", "バリュープライシング"]
        )
        
        base_price = st.number_input("基準価格", value=1000, step=100)
        
        if strategy_type == "ペネトレーション（低価格浸透）":
            price_multiplier = st.slider("価格倍率", 0.5, 1.0, 0.7, 0.05)
            demand_elasticity = -1.5  # 価格に敏感
        elif strategy_type == "スキミング（高価格戦略）":
            price_multiplier = st.slider("価格倍率", 1.0, 3.0, 2.0, 0.1)
            demand_elasticity = -0.8  # 価格に比較的鈍感
        elif strategy_type == "競合追従":
            price_multiplier = st.slider("価格倍率", 0.8, 1.2, 1.0, 0.05)
            demand_elasticity = -1.2  # 標準的な感度
        else:  # バリュープライシング
            price_multiplier = st.slider("価格倍率", 1.2, 2.5, 1.8, 0.1)
            demand_elasticity = -0.6  # 価値重視で価格に鈍感
    
    # シミュレーション実行
    actual_price = base_price * price_multiplier
    potential_customers = total_addressable_market * (market_penetration / 100)
    
    # 価格弾力性を考慮した需要計算
    price_effect = (price_multiplier - 1) * demand_elasticity
    adjusted_conversion_rate = base_conversion_rate * (1 + price_effect / 100)
    adjusted_conversion_rate = max(0.1, min(adjusted_conversion_rate, 50))  # 0.1%-50%で制限
    
    customers = potential_customers * (adjusted_conversion_rate / 100) / competition_factor
    monthly_revenue = customers * actual_price
    operational_costs = monthly_revenue * (operational_cost_ratio / 100)
    monthly_profit = monthly_revenue - operational_costs
    
    # 年間予測
    annual_revenue = monthly_revenue * 12
    annual_profit = monthly_profit * 12
    profit_margin = (monthly_profit / monthly_revenue * 100) if monthly_revenue > 0 else 0
    
    # 結果表示
    st.markdown("### 📊 シミュレーション結果")
    
    result_cols = st.columns(4)
    
    with result_cols[0]:
        st.metric(
            "月間売上",
            f"¥{monthly_revenue:,.0f}",
            delta=f"{((price_multiplier - 1) * 100):+.1f}% vs 基準"
        )
    
    with result_cols[1]:
        st.metric(
            "獲得顧客数",
            f"{customers:,.0f}人",
            delta=f"CV率: {adjusted_conversion_rate:.1f}%"
        )
    
    with result_cols[2]:
        st.metric(
            "月間利益",
            f"¥{monthly_profit:,.0f}",
            delta=f"利益率: {profit_margin:.1f}%"
        )
    
    with result_cols[3]:
        st.metric(
            "年間収益予測",
            f"¥{annual_revenue:,.0f}",
            delta=f"年間利益: ¥{annual_profit:,.0f}"
        )
    
    # 戦略比較グラフ
    st.markdown("### 📈 戦略比較分析")
    
    strategies_comparison = []
    strategy_names = ["ペネトレーション", "競合追従", "バリュープライシング", "スキミング"]
    price_multipliers = [0.7, 1.0, 1.8, 2.0]
    elasticities = [-1.5, -1.2, -0.6, -0.8]
    
    for i, (strat_name, mult, elasticity) in enumerate(zip(strategy_names, price_multipliers, elasticities)):
        strat_price = base_price * mult
        strat_price_effect = (mult - 1) * elasticity
        strat_conversion = base_conversion_rate * (1 + strat_price_effect / 100)
        strat_conversion = max(0.1, min(strat_conversion, 50))
        
        strat_customers = potential_customers * (strat_conversion / 100) / competition_factor
        strat_revenue = strat_customers * strat_price
        strat_costs = strat_revenue * (operational_cost_ratio / 100)
        strat_profit = strat_revenue - strat_costs
        
        strategies_comparison.append({
            'Strategy': strat_name,
            'Price': strat_price,
            'Customers': strat_customers,
            'Revenue': strat_revenue,
            'Profit': strat_profit,
            'Margin': (strat_profit / strat_revenue * 100) if strat_revenue > 0 else 0
        })
    
    df_comparison = pd.DataFrame(strategies_comparison)
    
    # グラフ作成
    fig_comparison = make_subplots(
        rows=2, cols=2,
        subplot_titles=('収益比較', '顧客数比較', '利益比較', '利益率比較'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # 収益比較
    fig_comparison.add_trace(
        go.Bar(x=df_comparison['Strategy'], y=df_comparison['Revenue'], name='収益'),
        row=1, col=1
    )
    
    # 顧客数比較
    fig_comparison.add_trace(
        go.Bar(x=df_comparison['Strategy'], y=df_comparison['Customers'], name='顧客数'),
        row=1, col=2
    )
    
    # 利益比較
    fig_comparison.add_trace(
        go.Bar(x=df_comparison['Strategy'], y=df_comparison['Profit'], name='利益'),
        row=2, col=1
    )
    
    # 利益率比較
    fig_comparison.add_trace(
        go.Bar(x=df_comparison['Strategy'], y=df_comparison['Margin'], name='利益率(%)'),
        row=2, col=2
    )
    
    fig_comparison.update_layout(
        height=600,
        showlegend=False,
        template='plotly_dark',
        title_text="価格戦略別パフォーマンス比較"
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # 詳細比較テーブル
    st.markdown("### 📋 詳細比較テーブル")
    
    # フォーマット済みデータフレーム作成
    df_display = df_comparison.copy()
    df_display['Price'] = df_display['Price'].apply(lambda x: f"¥{x:,.0f}")
    df_display['Customers'] = df_display['Customers'].apply(lambda x: f"{x:,.0f}人")
    df_display['Revenue'] = df_display['Revenue'].apply(lambda x: f"¥{x:,.0f}")
    df_display['Profit'] = df_display['Profit'].apply(lambda x: f"¥{x:,.0f}")
    df_display['Margin'] = df_display['Margin'].apply(lambda x: f"{x:.1f}%")
    
    df_display.columns = ['戦略', '価格', '顧客数', '月間売上', '月間利益', '利益率']
    st.dataframe(df_display, use_container_width=True)
    
    # 推奨戦略
    best_revenue_idx = df_comparison['Revenue'].idxmax()
    best_profit_idx = df_comparison['Profit'].idxmax()
    best_margin_idx = df_comparison['Margin'].idxmax()
    
    st.markdown("### 🏆 推奨戦略")
    
    rec_cols = st.columns(3)
    
    with rec_cols[0]:
        st.markdown(f"""
        <div class="result-highlight">
            <h4>💰 売上最大化</h4>
            <h3>{df_comparison.iloc[best_revenue_idx]['Strategy']}</h3>
            <p>月間売上: ¥{df_comparison.iloc[best_revenue_idx]['Revenue']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_cols[1]:
        st.markdown(f"""
        <div class="result-highlight">
            <h4>📈 利益最大化</h4>
            <h3>{df_comparison.iloc[best_profit_idx]['Strategy']}</h3>
            <p>月間利益: ¥{df_comparison.iloc[best_profit_idx]['Profit']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_cols[2]:
        st.markdown(f"""
        <div class="result-highlight">
            <h4>💎 効率最大化</h4>
            <h3>{df_comparison.iloc[best_margin_idx]['Strategy']}</h3>
            <p>利益率: {df_comparison.iloc[best_margin_idx]['Margin']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

# タブ5: 成長戦略
with tab5:
    st.markdown("## 📈 成長戦略ガイド")
    st.markdown("**段階的価格戦略とスケーリング計画**")
    
    # 成長段階別戦略
    st.markdown("### 🚀 成長段階別価格戦略")
    
    growth_stages = st.tabs(["🌱 Pre-PMF", "📈 Post-PMF", "🏢 スケーリング", "🌟 マーケットリーダー"])
    
    with growth_stages[0]:
        st.markdown("#### 🌱 Product-Market Fit前段階")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="strategy-card">
                <h4>🎯 主要目標</h4>
                <ul>
                    <li>PMFの検証</li>
                    <li>顧客フィードバック収集</li>
                    <li>プロダクト改善</li>
                    <li>初期ユーザー獲得</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="strategy-card">
                <h4>💰 価格戦略</h4>
                <ul>
                    <li><strong>フリーミアム</strong> or <strong>深度割引</strong></li>
                    <li>価格テストの実施</li>
                    <li>早期ユーザー特別価格</li>
                    <li>価値実証重視</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**📊 重要指標**: 利用継続率、NPS、機能利用率、ユーザーフィードバック数")
        
        # PMF検証チェックリスト
        st.markdown("**✅ PMF達成チェックリスト**")
        pmf_checks = [
            "ユーザーが能動的にプロダクトを利用している",
            "解約率が月5%以下を維持",
            "顧客から積極的なフィードバックがある",
            "口コミやオーガニック成長が見られる",
            "NPSスコアが50以上"
        ]
        
        for check in pmf_checks:
            st.checkbox(check, key=f"pmf_{check}")
    
    with growth_stages[1]:
        st.markdown("#### 📈 Product-Market Fit後段階")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="strategy-card">
                <h4>🎯 主要目標</h4>
                <ul>
                    <li>収益性の確立</li>
                    <li>持続可能な成長</li>
                    <li>マーケティング効率化</li>
                    <li>オペレーション最適化</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="strategy-card">
                <h4>💰 価格戦略</h4>
                <ul>
                    <li><strong>段階的価格上昇</strong></li>
                    <li>プラン多様化</li>
                    <li>アップセル機能追加</li>
                    <li>年間契約割引導入</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**📊 重要指標**: LTV/CAC、月次成長率、ARR、コホート分析")
        
        # 価格上昇シミュレーター
        st.markdown("**💹 段階的価格上昇プラン**")
        
        current_price = st.number_input("現在の価格", value=1000, key="postpmf_price")
        target_price = st.number_input("目標価格", value=2000, key="postpmf_target")
        months_to_target = st.slider("達成期間（月）", 3, 24, 12, key="postpmf_months")
        
        if target_price > current_price:
            monthly_increase = (target_price / current_price) ** (1/months_to_target) - 1
            
            price_schedule = []
            for month in range(months_to_target + 1):
                price = current_price * ((1 + monthly_increase) ** month)
                price_schedule.append({"Month": month, "Price": price})
            
            df_schedule = pd.DataFrame(price_schedule)
            
            fig_price_schedule = px.line(
                df_schedule, x="Month", y="Price",
                title="段階的価格上昇スケジュール",
                template="plotly_dark"
            )
            fig_price_schedule.update_traces(mode='markers+lines')
            st.plotly_chart(fig_price_schedule, use_container_width=True)
            
            st.info(f"📈 月次価格上昇率: {monthly_increase*100:.1f}% | 最終価格: ¥{target_price:,.0f}")
    
    with growth_stages[2]:
        st.markdown("#### 🏢 スケーリング段階")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="strategy-card">
                <h4>🎯 主要目標</h4>
                <ul>
                    <li>市場シェア拡大</li>
                    <li>企業顧客獲得</li>
                    <li>国際展開</li>
                    <li>プラットフォーム化</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="strategy-card">
                <h4>💰 価格戦略</h4>
                <ul>
                    <li><strong>セグメント別価格</strong></li>
                    <li>エンタープライズプラン</li>
                    <li>ボリューム割引</li>
                    <li>地域別価格戦略</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**📊 重要指標**: Market Share、Enterprise Win Rate、International Revenue、Partner Revenue")
        
        # セグメント別価格設定
        st.markdown("**🎯 セグメント別価格戦略**")
        
        segment_cols = st.columns(3)
        
        with segment_cols[0]:
            st.markdown("""
            <div class="calculator-box">
                <h4>👤 個人・スモールビジネス</h4>
                <p><strong>価格帯</strong>: ¥500-5,000/月</p>
                <p><strong>特徴</strong>: セルフサービス</p>
                <p><strong>重視指標</strong>: 価格・使いやすさ</p>
            </div>
            """, unsafe_allow_html=True)
        
        with segment_cols[1]:
            st.markdown("""
            <div class="calculator-box">
                <h4>🏢 中規模企業</h4>
                <p><strong>価格帯</strong>: ¥5,000-50,000/月</p>
                <p><strong>特徴</strong>: サポート付き</p>
                <p><strong>重視指標</strong>: 機能・統合性</p>
            </div>
            """, unsafe_allow_html=True)
        
        with segment_cols[2]:
            st.markdown("""
            <div class="calculator-box">
                <h4>🏭 大企業</h4>
                <p><strong>価格帯</strong>: ¥50,000+/月</p>
                <p><strong>特徴</strong>: カスタマイズ</p>
                <p><strong>重視指標</strong>: セキュリティ・SLA</p>
            </div>
            """, unsafe_allow_html=True)
    
    with growth_stages[3]:
        st.markdown("#### 🌟 マーケットリーダー段階")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="strategy-card">
                <h4>🎯 主要目標</h4>
                <ul>
                    <li>市場支配的地位維持</li>
                    <li>新市場創造</li>
                    <li>エコシステム構築</li>
                    <li>イノベーション継続</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="strategy-card">
                <h4>💰 価格戦略</h4>
                <ul>
                    <li><strong>プレミアム価格</strong></li>
                    <li>バンドル戦略</li>
                    <li>プラットフォーム料金</li>
                    <li>バリューベース価格</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**📊 重要指標**: Market Dominance、Innovation Rate、Platform Revenue、Customer Lifetime Value")
        
        # プレミアム価格戦略
        st.markdown("**👑 プレミアム価格戦略設計**")
        
        premium_factors = st.multiselect(
            "プレミアム価格を正当化する要素を選択:",
            [
                "独自技術・特許",
                "圧倒的ユーザーベース",
                "豊富なエコシステム",
                "高度なセキュリティ",
                "24/7プレミアムサポート",
                "高い信頼性・SLA",
                "業界認定・コンプライアンス",
                "カスタマイズ・統合機能"
            ],
            default=["独自技術・特許", "圧倒的ユーザーベース"]
        )
        
        if premium_factors:
            premium_multiplier = 1 + (len(premium_factors) * 0.15)
            st.info(f"🎯 推奨プレミアム倍率: {premium_multiplier:.1f}x (選択要素: {len(premium_factors)}個)")
            
            base_market_price = st.number_input("市場標準価格", value=10000)
            recommended_premium_price = base_market_price * premium_multiplier
            
            st.markdown(f"""
            <div class="result-highlight">
                <h4>💎 推奨プレミアム価格</h4>
                <h2>¥{recommended_premium_price:,.0f}</h2>
                <p>市場標準価格の{premium_multiplier:.1f}倍</p>
            </div>
            """, unsafe_allow_html=True)
    
    # A/Bテスト計画
    st.markdown("---")
    st.markdown("### 🧪 価格A/Bテスト計画")
    
    ab_test_cols = st.columns(2)
    
    with ab_test_cols[0]:
        st.markdown("""
        **📋 テスト設計のベストプラクティス**
        
        1. **単一変数テスト**: 価格のみを変更
        2. **統計的有意性**: 95%信頼度、80%検出力
        3. **適切なサンプルサイズ**: 最低1000ユーザー/グループ
        4. **テスト期間**: 最低2週間、理想的には1ヶ月
        5. **セグメント分析**: 顧客属性別の反応確認
        """)
    
    with ab_test_cols[1]:
        st.markdown("**🎯 A/Bテスト計算機**")
        
        current_conversion = st.slider("現在のコンバージョン率 (%)", 1.0, 20.0, 5.0, 0.1)
        expected_improvement = st.slider("期待する改善率 (%)", 5, 50, 20)
        confidence_level = st.selectbox("信頼度", [90, 95, 99], index=1)
        
        # サンプルサイズ計算（簡易版）
        from math import sqrt, log
        
        p1 = current_conversion / 100
        p2 = p1 * (1 + expected_improvement / 100)
        
        # Z値（簡易）
        z_alpha = 1.96 if confidence_level == 95 else (1.645 if confidence_level == 90 else 2.576)
        z_beta = 0.84  # 80% power
        
        pooled_p = (p1 + p2) / 2
        sample_size = (z_alpha * sqrt(2 * pooled_p * (1 - pooled_p)) + z_beta * sqrt(p1 * (1 - p1) + p2 * (1 - p2)))**2 / (p2 - p1)**2
        sample_size = int(sample_size) + 1
        
        test_duration_days = sample_size / (100)  # 1日100訪問者想定
        
        st.markdown(f"""
        <div class="result-highlight">
            <h4>📊 必要サンプルサイズ</h4>
            <p><strong>各グループ</strong>: {sample_size:,}人</p>
            <p><strong>テスト期間</strong>: {test_duration_days:.0f}日</p>
            <p><strong>期待結果</strong>: {p1*100:.1f}% → {p2*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

# フッター
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h3>🎯 価格戦略の成功のために</h3>
    <p>価格設定は継続的な最適化プロセスです。定期的な分析と調整で、ビジネス成長を加速させましょう。</p>
    <p><strong>🔗 関連ツール</strong>: 
        <a href="marketing_tools_list">広告マーケティングツール</a> | 
        <a href="analysis_tools_list">運営分析ツール</a> | 
        <a href="dev_tools_list">新規開発ツール</a>
    </p>
</div>
""", unsafe_allow_html=True)