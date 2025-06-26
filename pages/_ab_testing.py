#!/usr/bin/env python3
"""
A/Bテスト自動化ツール
テストの作成、実行、結果評価、統計的有意性の判定まで完全自動化
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
from scipy import stats
from typing import Dict, List, Any, Optional
import uuid

# ページ設定
st.set_page_config(
    page_title="A/Bテスト自動化",
    page_icon="🧪",
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
    
    /* テストカード */
    .test-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        transition: all 0.3s;
    }
    
    .test-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
    }
    
    .test-status {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .status-paused {
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
    }
    
    .status-completed {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
    }
    
    /* バリアントカード */
    .variant-card {
        background: rgba(30, 41, 59, 0.5);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin: 10px 0;
    }
    
    .variant-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .variant-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #3b82f6;
    }
    
    .variant-control {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
    }
    
    /* 結果カード */
    .result-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .result-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3b82f6;
        margin: 10px 0;
    }
    
    .result-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* 統計的有意性 */
    .significance-badge {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
    }
    
    .not-significant {
        background: rgba(107, 114, 128, 0.2);
        color: #6b7280;
    }
    
    /* 信頼区間バー */
    .confidence-bar {
        height: 8px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 4px;
        margin: 10px 0;
        position: relative;
    }
    
    .confidence-range {
        position: absolute;
        height: 100%;
        background: #3b82f6;
        border-radius: 4px;
    }
    
    .confidence-point {
        position: absolute;
        width: 3px;
        height: 16px;
        background: #10b981;
        top: -4px;
        border-radius: 2px;
    }
    
    /* 勝者バッジ */
    .winner-badge {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        display: inline-block;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'ab_tests' not in st.session_state:
    st.session_state.ab_tests = {}

if 'test_results' not in st.session_state:
    st.session_state.test_results = {}

class ABTest:
    """A/Bテストクラス"""
    
    def __init__(self, name: str, test_type: str, variants: List[Dict[str, Any]]):
        self.id = str(uuid.uuid4())
        self.name = name
        self.test_type = test_type
        self.variants = variants
        self.status = "active"
        self.created_at = datetime.now()
        self.start_date = datetime.now()
        self.end_date = None
        self.sample_size = 0
        self.confidence_level = 0.95
        self.minimum_detectable_effect = 0.05
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "test_type": self.test_type,
            "variants": self.variants,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "sample_size": self.sample_size,
            "confidence_level": self.confidence_level,
            "minimum_detectable_effect": self.minimum_detectable_effect
        }

def generate_test_data(test: ABTest, days: int = 7) -> pd.DataFrame:
    """テスト結果のサンプルデータを生成"""
    np.random.seed(42)
    
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    data = []
    
    for date in dates:
        for i, variant in enumerate(test.variants):
            # バリアントごとに異なる成果を設定
            base_conversion_rate = 0.03 + (i * 0.005)  # バリアントBの方が少し高い
            daily_visitors = np.random.poisson(1000)
            conversions = np.random.binomial(daily_visitors, base_conversion_rate)
            
            data.append({
                'date': date,
                'variant': variant['name'],
                'visitors': daily_visitors,
                'conversions': conversions,
                'conversion_rate': conversions / daily_visitors if daily_visitors > 0 else 0,
                'revenue': conversions * np.random.normal(5000, 1000)
            })
    
    return pd.DataFrame(data)

def calculate_statistical_significance(control_data: pd.DataFrame, variant_data: pd.DataFrame) -> Dict[str, Any]:
    """統計的有意性を計算"""
    # コンバージョン率の計算
    control_conversions = control_data['conversions'].sum()
    control_visitors = control_data['visitors'].sum()
    control_rate = control_conversions / control_visitors if control_visitors > 0 else 0
    
    variant_conversions = variant_data['conversions'].sum()
    variant_visitors = variant_data['visitors'].sum()
    variant_rate = variant_conversions / variant_visitors if variant_visitors > 0 else 0
    
    # 効果サイズ（リフト）
    lift = ((variant_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0
    
    # Z検定
    pooled_rate = (control_conversions + variant_conversions) / (control_visitors + variant_visitors)
    se = np.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_visitors + 1/variant_visitors))
    
    if se > 0:
        z_score = (variant_rate - control_rate) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    else:
        z_score = 0
        p_value = 1
    
    # 信頼区間の計算
    confidence_level = 0.95
    z_critical = stats.norm.ppf((1 + confidence_level) / 2)
    margin_of_error = z_critical * se
    ci_lower = (variant_rate - control_rate - margin_of_error) * 100
    ci_upper = (variant_rate - control_rate + margin_of_error) * 100
    
    # 検出力（パワー）の計算
    effect_size = abs(variant_rate - control_rate) / np.sqrt(pooled_rate * (1 - pooled_rate))
    sample_size = (control_visitors + variant_visitors) / 2
    power = 1 - stats.norm.cdf(z_critical - effect_size * np.sqrt(sample_size))
    
    return {
        'control_rate': control_rate,
        'variant_rate': variant_rate,
        'lift': lift,
        'p_value': p_value,
        'is_significant': p_value < 0.05,
        'confidence_interval': (ci_lower, ci_upper),
        'z_score': z_score,
        'power': power,
        'sample_size': {
            'control': control_visitors,
            'variant': variant_visitors
        }
    }

def calculate_sample_size_needed(baseline_rate: float, mde: float, power: float = 0.8, alpha: float = 0.05) -> int:
    """必要なサンプルサイズを計算"""
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    
    n = (2 * (z_alpha + z_beta)**2 * (p1*(1-p1) + p2*(1-p2))) / (p2 - p1)**2
    
    return int(np.ceil(n))

# ヘッダー
st.title("🧪 A/Bテスト自動化ツール")
st.caption("テストの作成から結果評価、統計的有意性の判定まで完全自動化")

# タブ構成
tabs = st.tabs(["🚀 実行中のテスト", "➕ 新規テスト作成", "📊 結果分析", "📈 過去のテスト", "🎯 サンプルサイズ計算"])

# 実行中のテストタブ
with tabs[0]:
    active_tests = {tid: test for tid, test in st.session_state.ab_tests.items() 
                    if test.status == "active"}
    
    if active_tests:
        for test_id, test in active_tests.items():
            st.markdown(f"""
            <div class="test-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: #e2e8f0; margin: 0;">{test.name}</h3>
                    <span class="test-status status-{test.status}">{test.status.upper()}</span>
                </div>
                <p style="color: #94a3b8; margin: 10px 0;">タイプ: {test.test_type} | 開始: {test.start_date.strftime('%Y-%m-%d')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # テストデータを生成
            test_data = generate_test_data(test)
            
            # バリアント別の結果表示
            col1, col2 = st.columns(2)
            
            for i, variant in enumerate(test.variants):
                variant_data = test_data[test_data['variant'] == variant['name']]
                
                with col1 if i == 0 else col2:
                    is_control = variant.get('is_control', False)
                    st.markdown(f"""
                    <div class="variant-card">
                        <div class="variant-header">
                            <span class="variant-name">{variant['name']}</span>
                            {"<span class='variant-control'>コントロール</span>" if is_control else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # メトリクス表示
                    total_visitors = variant_data['visitors'].sum()
                    total_conversions = variant_data['conversions'].sum()
                    avg_conversion_rate = (total_conversions / total_visitors * 100) if total_visitors > 0 else 0
                    total_revenue = variant_data['revenue'].sum()
                    
                    metrics_col1, metrics_col2 = st.columns(2)
                    
                    with metrics_col1:
                        st.metric("訪問者数", f"{total_visitors:,}")
                        st.metric("コンバージョン", f"{total_conversions:,}")
                    
                    with metrics_col2:
                        st.metric("CVR", f"{avg_conversion_rate:.2f}%")
                        st.metric("収益", f"¥{total_revenue:,.0f}")
            
            # アクションボタン
            action_col1, action_col2, action_col3 = st.columns(3)
            
            with action_col1:
                if st.button(f"⏸️ 一時停止", key=f"pause_{test_id}"):
                    test.status = "paused"
                    st.rerun()
            
            with action_col2:
                if st.button(f"✅ 完了", key=f"complete_{test_id}"):
                    test.status = "completed"
                    test.end_date = datetime.now()
                    st.rerun()
            
            with action_col3:
                if st.button(f"📊 詳細分析", key=f"analyze_{test_id}"):
                    st.session_state.selected_test_id = test_id
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info("実行中のA/Bテストはありません")
        st.markdown("""
        ### 🚀 A/Bテストを始めましょう
        
        A/Bテストは、マーケティング施策の効果を科学的に検証する最も確実な方法です。
        
        **テスト可能な要素:**
        - ランディングページのデザイン
        - CTAボタンの文言・色
        - 価格設定
        - メールの件名
        - 広告クリエイティブ
        """)

# 新規テスト作成タブ
with tabs[1]:
    st.header("新規A/Bテスト作成")
    
    with st.form("create_ab_test"):
        test_name = st.text_input("テスト名*", placeholder="例: ホームページCTAボタンテスト")
        
        test_type = st.selectbox(
            "テストタイプ*",
            ["ランディングページ", "メール", "広告", "価格", "機能", "その他"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            confidence_level = st.slider("信頼水準", 0.90, 0.99, 0.95, 0.01)
            minimum_detectable_effect = st.slider("最小検出効果 (MDE)", 0.01, 0.20, 0.05, 0.01)
        
        with col2:
            test_duration = st.number_input("テスト期間（日）", min_value=1, value=14)
            expected_daily_traffic = st.number_input("予想日次トラフィック", min_value=100, value=1000)
        
        st.markdown("### バリアント設定")
        
        # コントロール（A）
        st.markdown("#### バリアントA（コントロール）")
        control_name = st.text_input("名前", value="コントロール", key="control_name")
        control_description = st.text_area("説明", placeholder="現在のバージョンの説明", key="control_desc")
        
        # バリアント（B）
        st.markdown("#### バリアントB")
        variant_name = st.text_input("名前", value="バリアント", key="variant_name")
        variant_description = st.text_area("説明", placeholder="テストバージョンの説明", key="variant_desc")
        variant_hypothesis = st.text_area(
            "仮説",
            placeholder="例: CTAボタンの色を青から緑に変更することで、クリック率が10%向上する"
        )
        
        # サンプルサイズ計算
        baseline_rate = st.number_input("現在のコンバージョン率 (%)", min_value=0.1, max_value=100.0, value=3.0) / 100
        required_sample_size = calculate_sample_size_needed(baseline_rate, minimum_detectable_effect)
        days_needed = required_sample_size / (expected_daily_traffic * 2)  # 2バリアント
        
        st.info(f"""
        **推奨サンプルサイズ**: 各バリアント {required_sample_size:,} 訪問者
        **推定必要日数**: {days_needed:.1f} 日
        """)
        
        submitted = st.form_submit_button("テストを開始", type="primary", use_container_width=True)
        
        if submitted:
            if test_name:
                variants = [
                    {
                        "name": control_name,
                        "description": control_description,
                        "is_control": True
                    },
                    {
                        "name": variant_name,
                        "description": variant_description,
                        "hypothesis": variant_hypothesis,
                        "is_control": False
                    }
                ]
                
                new_test = ABTest(test_name, test_type, variants)
                new_test.confidence_level = confidence_level
                new_test.minimum_detectable_effect = minimum_detectable_effect
                
                st.session_state.ab_tests[new_test.id] = new_test
                st.success(f"A/Bテスト '{test_name}' を開始しました！")
                st.rerun()
            else:
                st.error("テスト名を入力してください")

# 結果分析タブ
with tabs[2]:
    st.header("📊 テスト結果分析")
    
    # 分析するテストを選択
    if st.session_state.ab_tests:
        test_names = {tid: test.name for tid, test in st.session_state.ab_tests.items()}
        
        selected_test_id = st.selectbox(
            "分析するテストを選択",
            options=list(test_names.keys()),
            format_func=lambda x: test_names[x],
            key="analysis_test_select"
        )
        
        if selected_test_id:
            test = st.session_state.ab_tests[selected_test_id]
            test_data = generate_test_data(test, days=14)
            
            # コントロールとバリアントのデータを分離
            control_data = test_data[test_data['variant'] == test.variants[0]['name']]
            variant_data = test_data[test_data['variant'] == test.variants[1]['name']]
            
            # 統計的有意性の計算
            results = calculate_statistical_significance(control_data, variant_data)
            
            # 結果サマリー
            st.markdown("### 🎯 結果サマリー")
            
            if results['is_significant']:
                if results['lift'] > 0:
                    st.markdown(f"""
                    <div class="winner-badge">
                        🏆 バリアントBが勝利！ +{results['lift']:.1f}%のリフト
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="winner-badge">
                        🏆 コントロールが勝利！ {abs(results['lift']):.1f}%の差
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="significance-badge not-significant">
                    統計的有意差なし
                </div>
                """, unsafe_allow_html=True)
            
            # 主要指標
            metrics_cols = st.columns(4)
            
            with metrics_cols[0]:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">コントロールCVR</div>
                    <div class="result-value">{results['control_rate']*100:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_cols[1]:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">バリアントCVR</div>
                    <div class="result-value">{results['variant_rate']*100:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_cols[2]:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">リフト</div>
                    <div class="result-value" style="color: {'#10b981' if results['lift'] > 0 else '#ef4444'};">
                        {results['lift']:+.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_cols[3]:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">p値</div>
                    <div class="result-value">{results['p_value']:.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # 詳細統計
            st.markdown("### 📈 詳細統計")
            
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.markdown("#### 統計的検定結果")
                st.write(f"**Z値**: {results['z_score']:.3f}")
                st.write(f"**信頼区間 (95%)**: {results['confidence_interval'][0]:.2f}% ~ {results['confidence_interval'][1]:.2f}%")
                st.write(f"**検出力**: {results['power']*100:.1f}%")
                
                # 信頼区間の視覚化
                ci_lower, ci_upper = results['confidence_interval']
                ci_center = (ci_lower + ci_upper) / 2
                ci_width = ci_upper - ci_lower
                
                st.markdown(f"""
                <div style="margin: 20px 0;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8;">
                        <span>{ci_lower:.1f}%</span>
                        <span>0%</span>
                        <span>{ci_upper:.1f}%</span>
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-range" style="left: {max(0, (ci_lower + 10) * 5)}%; width: {ci_width * 5}%;"></div>
                        <div class="confidence-point" style="left: 50%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with detail_col2:
                st.markdown("#### サンプルサイズ")
                st.write(f"**コントロール**: {results['sample_size']['control']:,} 訪問者")
                st.write(f"**バリアント**: {results['sample_size']['variant']:,} 訪問者")
                st.write(f"**合計**: {results['sample_size']['control'] + results['sample_size']['variant']:,} 訪問者")
                
                # パワー分析
                if results['power'] < 0.8:
                    st.warning("検出力が80%未満です。より多くのサンプルが必要かもしれません。")
                else:
                    st.success("十分な検出力があります。")
            
            # 時系列グラフ
            st.markdown("### 📊 コンバージョン率の推移")
            
            # 日別のコンバージョン率を計算
            daily_rates = test_data.groupby(['date', 'variant']).agg({
                'conversions': 'sum',
                'visitors': 'sum'
            }).reset_index()
            daily_rates['conversion_rate'] = daily_rates['conversions'] / daily_rates['visitors'] * 100
            
            fig = px.line(
                daily_rates,
                x='date',
                y='conversion_rate',
                color='variant',
                title="日別コンバージョン率",
                labels={'conversion_rate': 'CVR (%)', 'date': '日付'},
                color_discrete_map={
                    test.variants[0]['name']: '#ef4444',
                    test.variants[1]['name']: '#10b981'
                }
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 累積コンバージョンの比較
            cumulative_data = test_data.copy()
            cumulative_data['cumulative_conversions'] = cumulative_data.groupby('variant')['conversions'].cumsum()
            cumulative_data['cumulative_visitors'] = cumulative_data.groupby('variant')['visitors'].cumsum()
            cumulative_data['cumulative_cvr'] = cumulative_data['cumulative_conversions'] / cumulative_data['cumulative_visitors'] * 100
            
            fig2 = px.line(
                cumulative_data,
                x='date',
                y='cumulative_cvr',
                color='variant',
                title="累積コンバージョン率",
                labels={'cumulative_cvr': '累積CVR (%)', 'date': '日付'},
                color_discrete_map={
                    test.variants[0]['name']: '#ef4444',
                    test.variants[1]['name']: '#10b981'
                }
            )
            
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # 推奨アクション
            st.markdown("### 💡 推奨アクション")
            
            if results['is_significant']:
                if results['lift'] > 0:
                    st.success(f"""
                    **バリアントBを採用することを推奨します。**
                    
                    - 統計的に有意な{results['lift']:.1f}%の改善が確認されました
                    - p値（{results['p_value']:.4f}）は有意水準を下回っています
                    - 年間推定効果: {results['lift'] * 12:.0f}%の収益向上
                    """)
                else:
                    st.warning(f"""
                    **コントロール（現在のバージョン）を維持することを推奨します。**
                    
                    - バリアントBは{abs(results['lift']):.1f}%のパフォーマンス低下を示しました
                    - 変更による悪影響を避けるため、現状維持が賢明です
                    """)
            else:
                additional_days = max(1, int((required_sample_size * 2 - results['sample_size']['control'] - results['sample_size']['variant']) / (expected_daily_traffic * 2)))
                st.info(f"""
                **まだ結論を出すには早すぎます。**
                
                - 統計的有意差は検出されていません（p値: {results['p_value']:.4f}）
                - あと約{additional_days}日間テストを継続することを推奨します
                - より多くのデータが必要です
                """)
    else:
        st.info("分析するテストがありません")

# 過去のテストタブ
with tabs[3]:
    completed_tests = {tid: test for tid, test in st.session_state.ab_tests.items() 
                      if test.status == "completed"}
    
    if completed_tests:
        st.header("📚 過去のテスト結果")
        
        # テスト一覧
        for test_id, test in completed_tests.items():
            test_data = generate_test_data(test)
            control_data = test_data[test_data['variant'] == test.variants[0]['name']]
            variant_data = test_data[test_data['variant'] == test.variants[1]['name']]
            results = calculate_statistical_significance(control_data, variant_data)
            
            st.markdown(f"""
            <div class="test-card">
                <h4 style="color: #e2e8f0;">{test.name}</h4>
                <p style="color: #94a3b8;">
                    期間: {test.start_date.strftime('%Y-%m-%d')} ~ {test.end_date.strftime('%Y-%m-%d') if test.end_date else '進行中'}
                </p>
                <p>
                    結果: リフト {results['lift']:+.1f}% | 
                    p値: {results['p_value']:.4f} | 
                    {"✅ 有意" if results['is_significant'] else "❌ 有意差なし"}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("完了したテストはまだありません")

# サンプルサイズ計算タブ
with tabs[4]:
    st.header("🎯 サンプルサイズ計算機")
    
    st.markdown("""
    A/Bテストを開始する前に、統計的に有意な結果を得るために必要なサンプルサイズを計算しましょう。
    """)
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        calc_baseline = st.number_input(
            "現在のコンバージョン率 (%)",
            min_value=0.1,
            max_value=100.0,
            value=3.0,
            step=0.1,
            key="calc_baseline"
        )
        
        calc_mde = st.slider(
            "検出したい最小効果 (MDE) %",
            min_value=1,
            max_value=50,
            value=10,
            key="calc_mde"
        )
        
        calc_confidence = st.slider(
            "信頼水準",
            min_value=0.90,
            max_value=0.99,
            value=0.95,
            step=0.01,
            key="calc_confidence"
        )
    
    with calc_col2:
        calc_power = st.slider(
            "検出力",
            min_value=0.70,
            max_value=0.95,
            value=0.80,
            step=0.05,
            key="calc_power"
        )
        
        calc_daily_traffic = st.number_input(
            "予想日次トラフィック（全体）",
            min_value=100,
            value=2000,
            step=100,
            key="calc_daily_traffic"
        )
        
        calc_split = st.slider(
            "トラフィック分割比率 (%)",
            min_value=10,
            max_value=90,
            value=50,
            help="コントロールに割り当てる割合",
            key="calc_split"
        )
    
    # 計算実行
    sample_size = calculate_sample_size_needed(
        calc_baseline / 100,
        calc_mde / 100,
        calc_power,
        1 - calc_confidence
    )
    
    # コントロールとバリアントへの配分
    control_size = int(sample_size * calc_split / 100)
    variant_size = int(sample_size * (100 - calc_split) / 100)
    total_size = control_size + variant_size
    
    # 必要日数
    days_needed = total_size / calc_daily_traffic
    
    # 結果表示
    st.markdown("### 📊 計算結果")
    
    result_cols = st.columns(3)
    
    with result_cols[0]:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">必要サンプルサイズ</div>
            <div class="result-value">{total_size:,}</div>
            <div style="font-size: 0.9rem; color: #94a3b8; margin-top: 10px;">
                コントロール: {control_size:,}<br>
                バリアント: {variant_size:,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with result_cols[1]:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">推定必要日数</div>
            <div class="result-value">{days_needed:.1f}日</div>
            <div style="font-size: 0.9rem; color: #94a3b8; margin-top: 10px;">
                約{days_needed/7:.1f}週間
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with result_cols[2]:
        expected_lift = calc_baseline * calc_mde / 100
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">期待される改善</div>
            <div class="result-value">+{expected_lift:.2f}%</div>
            <div style="font-size: 0.9rem; color: #94a3b8; margin-top: 10px;">
                {calc_baseline:.1f}% → {calc_baseline + expected_lift:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ヒント
    st.info("""
    💡 **ヒント**:
    - サンプルサイズが大きすぎる場合は、MDEを上げることを検討してください
    - 検出力80%は一般的な基準ですが、重要な決定には90%以上を推奨します
    - 早期終了は統計的妥当性を損なう可能性があるため避けましょう
    """)

# サイドバー
with st.sidebar:
    st.header("🧪 A/Bテスト管理")
    
    # テスト統計
    if st.session_state.ab_tests:
        st.subheader("📊 テスト統計")
        
        active_count = len([t for t in st.session_state.ab_tests.values() if t.status == "active"])
        completed_count = len([t for t in st.session_state.ab_tests.values() if t.status == "completed"])
        
        st.metric("実行中", active_count)
        st.metric("完了", completed_count)
        st.metric("合計", len(st.session_state.ab_tests))
    
    st.markdown("---")
    
    # ベストプラクティス
    st.subheader("📚 ベストプラクティス")
    
    st.markdown("""
    **1. 明確な仮説を立てる**
    - 何を変更し、どんな効果を期待するか
    
    **2. 十分なサンプルサイズ**
    - 統計的有意性を確保
    
    **3. テスト期間を守る**
    - 早期終了は避ける
    
    **4. 一度に1つの変更**
    - 効果の原因を特定可能に
    
    **5. 実装の検証**
    - テストが正しく動作しているか確認
    """)
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("📊 プロジェクト管理室", use_container_width=True):
        st.switch_page("pages/project_management.py")
    
    if st.button("📈 パフォーマンス", use_container_width=True):
        st.switch_page("pages/performance_dashboard.py")

# フッター
st.markdown("---")
st.caption("💡 ヒント: A/Bテストは科学的なアプローチでマーケティングを改善する最良の方法です。小さな改善の積み重ねが大きな成果につながります。")