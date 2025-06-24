#!/usr/bin/env python3
"""
アトリビューション分析・ROI最適化システム
高度な顧客ジャーニー分析とマルチタッチアトリビューション
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
from scipy import stats
import networkx as nx

# ページ設定
st.set_page_config(
    page_title="アトリビューション分析",
    page_icon="🎯",
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
    .attribution-header {
        background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .attribution-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(ellipse at center, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: attributionPulse 6s ease-in-out infinite;
    }
    
    @keyframes attributionPulse {
        0%, 100% { transform: scale(0.9) rotate(0deg); opacity: 0.3; }
        50% { transform: scale(1.1) rotate(180deg); opacity: 0.7; }
    }
    
    .attribution-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .attribution-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* アトリビューションカード */
    .attribution-card {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 2px solid rgba(139, 92, 246, 0.3);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .attribution-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .attribution-card:hover::before {
        left: 100%;
    }
    
    .attribution-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.4);
        border-color: #8b5cf6;
    }
    
    /* タッチポイント */
    .touchpoint {
        background: rgba(30, 41, 59, 0.8);
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 4px solid #8b5cf6;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }
    
    .touchpoint:hover {
        background: rgba(30, 41, 59, 1);
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.3);
    }
    
    .touchpoint-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .touchpoint-name {
        font-weight: bold;
        color: #8b5cf6;
        font-size: 1.1rem;
    }
    
    .touchpoint-contribution {
        background: rgba(139, 92, 246, 0.2);
        color: #8b5cf6;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* アトリビューションモデル */
    .attribution-model {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin: 15px 0;
        transition: all 0.3s;
    }
    
    .attribution-model:hover {
        border-color: rgba(139, 92, 246, 0.6);
        background: rgba(30, 41, 59, 0.8);
    }
    
    .model-active {
        border-color: #8b5cf6;
        background: rgba(139, 92, 246, 0.1);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.2);
    }
    
    .model-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #8b5cf6;
        margin-bottom: 10px;
    }
    
    .model-description {
        color: #94a3b8;
        margin-bottom: 15px;
    }
    
    .model-impact {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .impact-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #10b981;
    }
    
    /* カスタマージャーニー */
    .journey-step {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid rgba(139, 92, 246, 0.3);
        position: relative;
        transition: all 0.3s;
    }
    
    .journey-step:hover {
        border-color: rgba(139, 92, 246, 0.6);
        transform: translateY(-3px);
    }
    
    .journey-step::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 50%;
        transform: translateY(-50%);
        width: 12px;
        height: 12px;
        background: #8b5cf6;
        border-radius: 50%;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.3);
    }
    
    .step-number {
        background: #8b5cf6;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 15px;
        font-size: 0.9rem;
    }
    
    .step-info {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .step-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #e2e8f0;
    }
    
    .step-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    
    .step-metric {
        background: rgba(139, 92, 246, 0.1);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #8b5cf6;
        margin-bottom: 3px;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    /* ROI分析 */
    .roi-metric {
        background: rgba(30, 41, 59, 0.8);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(139, 92, 246, 0.3);
        transition: all 0.3s;
    }
    
    .roi-metric:hover {
        border-color: rgba(139, 92, 246, 0.6);
        transform: translateY(-5px);
    }
    
    .roi-value {
        font-size: 3rem;
        font-weight: bold;
        color: #8b5cf6;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
    }
    
    .roi-label {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    
    .roi-change {
        font-size: 0.9rem;
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .roi-positive {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .roi-negative {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    /* 統計的有意性 */
    .significance-test {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px solid rgba(139, 92, 246, 0.3);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
    }
    
    .test-result {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 15px 0;
    }
    
    .test-metric {
        text-align: center;
    }
    
    .test-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #8b5cf6;
    }
    
    .test-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    .significance-indicator {
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
    }
    
    .significant {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .not-significant {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* データ品質インジケーター */
    .data-quality {
        background: rgba(30, 41, 59, 0.6);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #8b5cf6;
        margin: 15px 0;
    }
    
    .quality-score {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .quality-bar {
        flex-grow: 1;
        height: 8px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .quality-fill {
        height: 100%;
        background: linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%);
        border-radius: 4px;
        transition: width 1s ease;
    }
    
    /* 予測モデル */
    .prediction-model {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin: 20px 0;
    }
    
    .prediction-confidence {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 15px;
    }
    
    .confidence-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: conic-gradient(#8b5cf6 0deg, #3b82f6 180deg, rgba(30, 41, 59, 0.5) 360deg);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    /* インサイトカード */
    .insight-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        transition: all 0.3s;
    }
    
    .insight-card:hover {
        border-color: rgba(139, 92, 246, 0.6);
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
    }
    
    .insight-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .insight-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #8b5cf6;
        margin-bottom: 10px;
    }
    
    /* ファネル最適化 */
    .funnel-optimization {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin: 20px 0;
    }
    
    .funnel-step {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .funnel-step:last-child {
        border-bottom: none;
    }
    
    .funnel-conversion {
        font-size: 1.2rem;
        font-weight: bold;
        color: #8b5cf6;
    }
    
    .funnel-improvement {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'attribution_data' not in st.session_state:
    st.session_state.attribution_data = {}

if 'attribution_models' not in st.session_state:
    st.session_state.attribution_models = {}

if 'customer_journeys' not in st.session_state:
    st.session_state.customer_journeys = []

def generate_customer_journey_data():
    """顧客ジャーニーデータを生成"""
    touchpoints = [
        {"name": "Google Search", "type": "Paid Search", "channel": "SEM"},
        {"name": "Facebook Ad", "type": "Social Media", "channel": "Social"},
        {"name": "Email Campaign", "type": "Email", "channel": "Email"},
        {"name": "Organic Search", "type": "Organic", "channel": "SEO"},
        {"name": "Display Ad", "type": "Display", "channel": "Display"},
        {"name": "YouTube Video", "type": "Video", "channel": "Video"},
        {"name": "LinkedIn Ad", "type": "Social Media", "channel": "Social"},
        {"name": "Direct Visit", "type": "Direct", "channel": "Direct"}
    ]
    
    journeys = []
    for i in range(50):  # 50の顧客ジャーニーを生成
        journey_length = np.random.randint(2, 6)
        journey_touchpoints = np.random.choice(touchpoints, journey_length, replace=False).tolist()
        
        # 各タッチポイントに時間とコストを追加
        for j, tp in enumerate(journey_touchpoints):
            tp['timestamp'] = datetime.now() - timedelta(days=np.random.randint(0, 30), hours=np.random.randint(0, 24))
            tp['cost'] = np.random.uniform(100, 2000)
            tp['position'] = j + 1
        
        journey = {
            'id': f"journey_{i+1}",
            'customer_id': f"customer_{i+1}",
            'touchpoints': journey_touchpoints,
            'conversion_value': np.random.uniform(5000, 50000),
            'conversion_date': datetime.now() - timedelta(days=np.random.randint(0, 7)),
            'converted': np.random.choice([True, False], p=[0.7, 0.3])
        }
        
        journeys.append(journey)
    
    return journeys

def calculate_attribution_models(journeys):
    """各アトリビューションモデルの結果を計算"""
    models = {
        'First-Touch': {},
        'Last-Touch': {},
        'Linear': {},
        'Time-Decay': {},
        'U-Shaped': {},
        'W-Shaped': {},
        'Custom ML': {}
    }
    
    for journey in journeys:
        if not journey['converted']:
            continue
            
        touchpoints = journey['touchpoints']
        conversion_value = journey['conversion_value']
        
        if len(touchpoints) == 0:
            continue
        
        # First-Touch Attribution
        first_tp = touchpoints[0]['name']
        models['First-Touch'][first_tp] = models['First-Touch'].get(first_tp, 0) + conversion_value
        
        # Last-Touch Attribution
        last_tp = touchpoints[-1]['name']
        models['Last-Touch'][last_tp] = models['Last-Touch'].get(last_tp, 0) + conversion_value
        
        # Linear Attribution
        value_per_touchpoint = conversion_value / len(touchpoints)
        for tp in touchpoints:
            tp_name = tp['name']
            models['Linear'][tp_name] = models['Linear'].get(tp_name, 0) + value_per_touchpoint
        
        # Time-Decay Attribution
        total_weight = sum(2**i for i in range(len(touchpoints)))
        for i, tp in enumerate(touchpoints):
            weight = 2**i / total_weight
            tp_name = tp['name']
            models['Time-Decay'][tp_name] = models['Time-Decay'].get(tp_name, 0) + (conversion_value * weight)
        
        # U-Shaped Attribution (40% first, 40% last, 20% middle)
        if len(touchpoints) == 1:
            tp_name = touchpoints[0]['name']
            models['U-Shaped'][tp_name] = models['U-Shaped'].get(tp_name, 0) + conversion_value
        elif len(touchpoints) == 2:
            for tp in touchpoints:
                tp_name = tp['name']
                models['U-Shaped'][tp_name] = models['U-Shaped'].get(tp_name, 0) + (conversion_value * 0.5)
        else:
            # First touchpoint: 40%
            first_tp = touchpoints[0]['name']
            models['U-Shaped'][first_tp] = models['U-Shaped'].get(first_tp, 0) + (conversion_value * 0.4)
            
            # Last touchpoint: 40%
            last_tp = touchpoints[-1]['name']
            models['U-Shaped'][last_tp] = models['U-Shaped'].get(last_tp, 0) + (conversion_value * 0.4)
            
            # Middle touchpoints: 20% split
            middle_touchpoints = touchpoints[1:-1]
            if middle_touchpoints:
                value_per_middle = (conversion_value * 0.2) / len(middle_touchpoints)
                for tp in middle_touchpoints:
                    tp_name = tp['name']
                    models['U-Shaped'][tp_name] = models['U-Shaped'].get(tp_name, 0) + value_per_middle
        
        # Custom ML Model (シミュレーション)
        ml_weights = np.random.dirichlet(np.ones(len(touchpoints)), size=1)[0]
        for i, tp in enumerate(touchpoints):
            tp_name = tp['name']
            models['Custom ML'][tp_name] = models['Custom ML'].get(tp_name, 0) + (conversion_value * ml_weights[i])
    
    return models

def calculate_roi_metrics(attribution_results, touchpoint_costs):
    """ROIメトリクスを計算"""
    roi_metrics = {}
    
    for model_name, attributions in attribution_results.items():
        model_roi = {}
        
        for touchpoint, attributed_value in attributions.items():
            cost = touchpoint_costs.get(touchpoint, 1000)  # デフォルトコスト
            roi = (attributed_value - cost) / cost * 100 if cost > 0 else 0
            roas = attributed_value / cost if cost > 0 else 0
            
            model_roi[touchpoint] = {
                'attributed_value': attributed_value,
                'cost': cost,
                'roi': roi,
                'roas': roas
            }
        
        roi_metrics[model_name] = model_roi
    
    return roi_metrics

def perform_statistical_significance_test(model1_data, model2_data):
    """統計的有意性テストを実行"""
    # サンプルデータから統計値を計算
    values1 = list(model1_data.values())
    values2 = list(model2_data.values())
    
    if len(values1) < 2 or len(values2) < 2:
        return {
            'p_value': 1.0,
            'significant': False,
            'test_statistic': 0,
            'confidence_interval': (0, 0),
            'effect_size': 0
        }
    
    # T-test
    t_stat, p_value = stats.ttest_ind(values1, values2)
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((len(values1)-1)*np.var(values1) + (len(values2)-1)*np.var(values2)) / (len(values1)+len(values2)-2))
    effect_size = (np.mean(values1) - np.mean(values2)) / pooled_std if pooled_std > 0 else 0
    
    # Confidence interval
    se = pooled_std * np.sqrt(1/len(values1) + 1/len(values2))
    margin_error = stats.t.ppf(0.975, len(values1)+len(values2)-2) * se
    mean_diff = np.mean(values1) - np.mean(values2)
    ci = (mean_diff - margin_error, mean_diff + margin_error)
    
    return {
        'p_value': abs(p_value),
        'significant': abs(p_value) < 0.05,
        'test_statistic': abs(t_stat),
        'confidence_interval': ci,
        'effect_size': abs(effect_size)
    }

# データ生成
customer_journeys = generate_customer_journey_data()
attribution_results = calculate_attribution_models(customer_journeys)

# タッチポイントコスト（仮想データ）
touchpoint_costs = {
    'Google Search': 5000,
    'Facebook Ad': 3000,
    'Email Campaign': 500,
    'Organic Search': 0,
    'Display Ad': 2000,
    'YouTube Video': 4000,
    'LinkedIn Ad': 3500,
    'Direct Visit': 0
}

roi_metrics = calculate_roi_metrics(attribution_results, touchpoint_costs)

# ヘッダー
st.markdown("""
<div class="attribution-header">
    <div class="attribution-title">🎯 アトリビューション分析・ROI最適化</div>
    <div class="attribution-subtitle">高度な顧客ジャーニー分析とマルチタッチアトリビューションによる究極のROI最適化</div>
</div>
""", unsafe_allow_html=True)

# 主要メトリクス
col1, col2, col3, col4, col5 = st.columns(5)

total_conversions = sum(1 for j in customer_journeys if j['converted'])
total_revenue = sum(j['conversion_value'] for j in customer_journeys if j['converted'])
total_cost = sum(touchpoint_costs.values())
overall_roi = ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
avg_touchpoints = np.mean([len(j['touchpoints']) for j in customer_journeys])

with col1:
    st.markdown(f"""
    <div class="roi-metric">
        <div class="roi-value">{total_conversions}</div>
        <div class="roi-label">総コンバージョン</div>
        <div class="roi-change roi-positive">+12.3%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="roi-metric">
        <div class="roi-value">¥{total_revenue:,.0f}</div>
        <div class="roi-label">総収益</div>
        <div class="roi-change roi-positive">+18.7%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="roi-metric">
        <div class="roi-value">{overall_roi:.1f}%</div>
        <div class="roi-label">総合ROI</div>
        <div class="roi-change roi-positive">+23.5%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="roi-metric">
        <div class="roi-value">{avg_touchpoints:.1f}</div>
        <div class="roi-label">平均タッチポイント</div>
        <div class="roi-change roi-positive">+0.3</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    overall_roas = total_revenue / total_cost if total_cost > 0 else 0
    st.markdown(f"""
    <div class="roi-metric">
        <div class="roi-value">{overall_roas:.1f}x</div>
        <div class="roi-label">総合ROAS</div>
        <div class="roi-change roi-positive">+0.8x</div>
    </div>
    """, unsafe_allow_html=True)

# タブ構成
tabs = st.tabs(["📊 アトリビューションモデル", "🛤️ カスタマージャーニー", "📈 ROI分析", "🔬 統計的検定", "🤖 予測分析"])

# アトリビューションモデルタブ
with tabs[0]:
    st.markdown("### 📊 アトリビューションモデル比較")
    
    # モデル選択
    col1, col2 = st.columns(2)
    
    with col1:
        selected_model = st.selectbox(
            "メインモデル選択",
            list(attribution_results.keys()),
            index=0
        )
    
    with col2:
        comparison_model = st.selectbox(
            "比較モデル選択",
            list(attribution_results.keys()),
            index=1
        )
    
    # モデル結果表示
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {selected_model} モデル結果")
        
        model_data = attribution_results[selected_model]
        sorted_touchpoints = sorted(model_data.items(), key=lambda x: x[1], reverse=True)
        
        for touchpoint, value in sorted_touchpoints:
            percentage = (value / sum(model_data.values()) * 100) if sum(model_data.values()) > 0 else 0
            
            st.markdown(f"""
            <div class="touchpoint">
                <div class="touchpoint-header">
                    <span class="touchpoint-name">{touchpoint}</span>
                    <span class="touchpoint-contribution">{percentage:.1f}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>貢献価値: ¥{value:,.0f}</div>
                    <div>ROI: {roi_metrics[selected_model].get(touchpoint, {}).get('roi', 0):.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"#### {comparison_model} モデル結果")
        
        comparison_data = attribution_results[comparison_model]
        sorted_comparison = sorted(comparison_data.items(), key=lambda x: x[1], reverse=True)
        
        for touchpoint, value in sorted_comparison:
            percentage = (value / sum(comparison_data.values()) * 100) if sum(comparison_data.values()) > 0 else 0
            
            st.markdown(f"""
            <div class="touchpoint">
                <div class="touchpoint-header">
                    <span class="touchpoint-name">{touchpoint}</span>
                    <span class="touchpoint-contribution">{percentage:.1f}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>貢献価値: ¥{value:,.0f}</div>
                    <div>ROI: {roi_metrics[comparison_model].get(touchpoint, {}).get('roi', 0):.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # モデル比較グラフ
    st.markdown("### 📈 モデル別貢献度比較")
    
    # データ準備
    touchpoints = list(set(list(model_data.keys()) + list(comparison_data.keys())))
    model1_values = [model_data.get(tp, 0) for tp in touchpoints]
    model2_values = [comparison_data.get(tp, 0) for tp in touchpoints]
    
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name=selected_model,
        x=touchpoints,
        y=model1_values,
        marker_color='rgba(139, 92, 246, 0.8)'
    ))
    
    fig_comparison.add_trace(go.Bar(
        name=comparison_model,
        x=touchpoints,
        y=model2_values,
        marker_color='rgba(59, 130, 246, 0.8)'
    ))
    
    fig_comparison.update_layout(
        title="アトリビューションモデル別貢献度比較",
        xaxis_title="タッチポイント",
        yaxis_title="貢献価値 (¥)",
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # モデル説明
    st.markdown("### 📚 アトリビューションモデル説明")
    
    model_descriptions = {
        'First-Touch': {
            'description': '最初のタッチポイントに100%の貢献を割り当て',
            'use_case': 'ブランド認知やアウェアネス施策の評価に適している',
            'pros': '新規顧客獲得への貢献が明確',
            'cons': 'コンバージョンに近いタッチポイントを過小評価'
        },
        'Last-Touch': {
            'description': '最後のタッチポイントに100%の貢献を割り当て',
            'use_case': 'ダイレクトレスポンス広告やクロージング施策の評価',
            'pros': 'コンバージョンに直結する要因が明確',
            'cons': 'アシスト効果のあるタッチポイントを無視'
        },
        'Linear': {
            'description': '全てのタッチポイントに均等に貢献を分配',
            'use_case': '全タッチポイントの貢献を公平に評価したい場合',
            'pros': 'すべてのタッチポイントが評価される',
            'cons': 'タッチポイントの重要度差が考慮されない'
        },
        'Time-Decay': {
            'description': 'コンバージョンに近いタッチポイントほど高い貢献度',
            'use_case': '短期間の購買検討プロセスの分析',
            'pros': '時間的な影響度を考慮',
            'cons': '長期的なブランディング効果を過小評価'
        },
        'U-Shaped': {
            'description': '最初と最後のタッチポイントを重視（各40%）',
            'use_case': 'アウェアネスとクロージングの両方を重視',
            'pros': '認知とコンバージョンのバランス評価',
            'cons': '中間タッチポイントの評価が低い'
        },
        'Custom ML': {
            'description': '機械学習による動的な貢献度算出',
            'use_case': '複雑な顧客ジャーニーの高精度分析',
            'pros': 'データドリブンで最適化',
            'cons': 'ブラックボックス化、解釈が困難'
        }
    }
    
    for model, info in model_descriptions.items():
        is_active = model in [selected_model, comparison_model]
        model_class = "attribution-model model-active" if is_active else "attribution-model"
        
        st.markdown(f"""
        <div class="{model_class}">
            <div class="model-name">{model}</div>
            <div class="model-description">{info['description']}</div>
            <div style="margin: 10px 0;">
                <strong>適用場面:</strong> {info['use_case']}<br>
                <strong>メリット:</strong> {info['pros']}<br>
                <strong>デメリット:</strong> {info['cons']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# カスタマージャーニータブ
with tabs[1]:
    st.markdown("### 🛤️ カスタマージャーニー分析")
    
    # ジャーニー分析設定
    col1, col2, col3 = st.columns(3)
    
    with col1:
        journey_filter = st.selectbox(
            "フィルター条件",
            ["全て", "コンバージョン済み", "未コンバージョン"]
        )
    
    with col2:
        min_touchpoints = st.slider("最小タッチポイント数", 1, 6, 2)
    
    with col3:
        max_touchpoints = st.slider("最大タッチポイント数", 2, 8, 6)
    
    # ジャーニーデータのフィルタリング
    filtered_journeys = customer_journeys.copy()
    
    if journey_filter == "コンバージョン済み":
        filtered_journeys = [j for j in filtered_journeys if j['converted']]
    elif journey_filter == "未コンバージョン":
        filtered_journeys = [j for j in filtered_journeys if not j['converted']]
    
    filtered_journeys = [j for j in filtered_journeys if min_touchpoints <= len(j['touchpoints']) <= max_touchpoints]
    
    # ジャーニーパターン分析
    st.markdown("#### 📊 ジャーニーパターン分析")
    
    # 最も一般的なジャーニーパス
    journey_paths = {}
    for journey in filtered_journeys:
        path = " → ".join([tp['name'] for tp in journey['touchpoints']])
        journey_paths[path] = journey_paths.get(path, 0) + 1
    
    top_paths = sorted(journey_paths.items(), key=lambda x: x[1], reverse=True)[:5]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🏆 最頻出ジャーニーパス")
        
        for i, (path, count) in enumerate(top_paths, 1):
            percentage = (count / len(filtered_journeys) * 100) if filtered_journeys else 0
            
            st.markdown(f"""
            <div class="journey-step">
                <div class="step-info">
                    <span class="step-number">{i}</span>
                    <span class="step-title">{path}</span>
                </div>
                <div style="margin-top: 10px;">
                    <strong>出現回数:</strong> {count}回 ({percentage:.1f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # ジャーニー長分布
        journey_lengths = [len(j['touchpoints']) for j in filtered_journeys]
        length_counts = pd.Series(journey_lengths).value_counts().sort_index()
        
        fig_length = px.bar(
            x=length_counts.index,
            y=length_counts.values,
            title="ジャーニー長分布",
            labels={'x': 'タッチポイント数', 'y': 'ジャーニー数'},
            color=length_counts.values,
            color_continuous_scale="Viridis"
        )
        
        fig_length.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        st.plotly_chart(fig_length, use_container_width=True)
    
    # タッチポイント遷移分析
    st.markdown("#### 🔄 タッチポイント遷移分析")
    
    # 遷移マトリックス作成
    touchpoint_names = list(touchpoint_costs.keys())
    transition_matrix = np.zeros((len(touchpoint_names), len(touchpoint_names)))
    
    for journey in filtered_journeys:
        touchpoints = [tp['name'] for tp in journey['touchpoints']]
        for i in range(len(touchpoints) - 1):
            from_idx = touchpoint_names.index(touchpoints[i])
            to_idx = touchpoint_names.index(touchpoints[i + 1])
            transition_matrix[from_idx][to_idx] += 1
    
    # 遷移確率に変換
    row_sums = transition_matrix.sum(axis=1, keepdims=True)
    transition_probs = np.divide(transition_matrix, row_sums, out=np.zeros_like(transition_matrix), where=row_sums!=0)
    
    # ヒートマップ
    fig_transition = px.imshow(
        transition_probs,
        x=touchpoint_names,
        y=touchpoint_names,
        color_continuous_scale="Viridis",
        title="タッチポイント遷移確率マトリックス"
    )
    
    fig_transition.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_transition, use_container_width=True)
    
    # 個別ジャーニー詳細表示
    st.markdown("#### 🔍 個別ジャーニー分析")
    
    if filtered_journeys:
        selected_journey_idx = st.selectbox(
            "分析するジャーニーを選択",
            range(len(filtered_journeys)),
            format_func=lambda x: f"Journey {x+1} - {'Converted' if filtered_journeys[x]['converted'] else 'Not Converted'} - {len(filtered_journeys[x]['touchpoints'])} touchpoints"
        )
        
        selected_journey = filtered_journeys[selected_journey_idx]
        
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">ジャーニー詳細</div>
            <div>
                <strong>顧客ID:</strong> {selected_journey['customer_id']}<br>
                <strong>コンバージョン:</strong> {'済み' if selected_journey['converted'] else '未'}<br>
                <strong>コンバージョン価値:</strong> ¥{selected_journey['conversion_value']:,.0f}<br>
                <strong>タッチポイント数:</strong> {len(selected_journey['touchpoints'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # タッチポイント詳細
        for i, touchpoint in enumerate(selected_journey['touchpoints'], 1):
            time_since_start = (touchpoint['timestamp'] - selected_journey['touchpoints'][0]['timestamp']).days
            
            st.markdown(f"""
            <div class="journey-step">
                <div class="step-info">
                    <span class="step-number">{i}</span>
                    <span class="step-title">{touchpoint['name']} ({touchpoint['channel']})</span>
                </div>
                <div class="step-metrics">
                    <div class="step-metric">
                        <div class="metric-value">¥{touchpoint['cost']:,.0f}</div>
                        <div class="metric-label">コスト</div>
                    </div>
                    <div class="step-metric">
                        <div class="metric-value">{time_since_start}</div>
                        <div class="metric-label">開始からの日数</div>
                    </div>
                    <div class="step-metric">
                        <div class="metric-value">{touchpoint['timestamp'].strftime('%m/%d')}</div>
                        <div class="metric-label">接触日</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ROI分析タブ
with tabs[2]:
    st.markdown("### 📈 ROI分析ダッシュボード")
    
    # ROIランキング
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 タッチポイント別ROIランキング")
        
        # 選択されたモデルのROIデータ
        model_roi = roi_metrics[selected_model]
        sorted_roi = sorted(model_roi.items(), key=lambda x: x[1]['roi'], reverse=True)
        
        for i, (touchpoint, metrics) in enumerate(sorted_roi, 1):
            roi_value = metrics['roi']
            roi_class = "roi-positive" if roi_value > 0 else "roi-negative"
            
            st.markdown(f"""
            <div class="touchpoint">
                <div class="touchpoint-header">
                    <span style="display: flex; align-items: center; gap: 10px;">
                        <span style="background: #8b5cf6; color: white; width: 25px; height: 25px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold;">{i}</span>
                        <span class="touchpoint-name">{touchpoint}</span>
                    </span>
                    <span class="touchpoint-contribution {roi_class}">{roi_value:+.1f}%</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;">
                    <div style="text-align: center;">
                        <div style="color: #8b5cf6; font-weight: bold;">¥{metrics['attributed_value']:,.0f}</div>
                        <div style="color: #94a3b8; font-size: 0.8rem;">貢献価値</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #ef4444; font-weight: bold;">¥{metrics['cost']:,.0f}</div>
                        <div style="color: #94a3b8; font-size: 0.8rem;">コスト</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #10b981; font-weight: bold;">{metrics['roas']:.1f}x</div>
                        <div style="color: #94a3b8; font-size: 0.8rem;">ROAS</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 ROI vs ROAS散布図")
        
        # 散布図データ準備
        touchpoints_list = []
        roi_values = []
        roas_values = []
        costs = []
        attributed_values = []
        
        for touchpoint, metrics in model_roi.items():
            touchpoints_list.append(touchpoint)
            roi_values.append(metrics['roi'])
            roas_values.append(metrics['roas'])
            costs.append(metrics['cost'])
            attributed_values.append(metrics['attributed_value'])
        
        fig_scatter = px.scatter(
            x=roi_values,
            y=roas_values,
            size=costs,
            color=attributed_values,
            hover_name=touchpoints_list,
            labels={'x': 'ROI (%)', 'y': 'ROAS (x)', 'color': '貢献価値'},
            title="ROI vs ROAS 散布図",
            color_continuous_scale="Viridis"
        )
        
        # 基準線を追加
        fig_scatter.add_hline(y=1, line_dash="dash", line_color="rgba(255,255,255,0.5)")
        fig_scatter.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.5)")
        
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # ROI最適化推奨
    st.markdown("#### 💡 ROI最適化推奨事項")
    
    # 最適化推奨を生成
    optimization_recommendations = []
    
    for touchpoint, metrics in model_roi.items():
        roi = metrics['roi']
        roas = metrics['roas']
        cost = metrics['cost']
        
        if roi < 0:
            optimization_recommendations.append({
                'touchpoint': touchpoint,
                'type': 'urgent',
                'action': '予算削減または停止',
                'reason': f'ROI {roi:.1f}% と損失状態',
                'impact': f'月間 ¥{abs(roi * cost / 100):,.0f} の損失削減'
            })
        elif roi < 50:
            optimization_recommendations.append({
                'touchpoint': touchpoint,
                'type': 'optimize',
                'action': 'キャンペーン最適化',
                'reason': f'ROI {roi:.1f}% と低パフォーマンス',
                'impact': f'最適化により {roi * 1.5:.1f}% ROI達成可能'
            })
        elif roi > 200:
            optimization_recommendations.append({
                'touchpoint': touchpoint,
                'type': 'scale',
                'action': '予算増額',
                'reason': f'ROI {roi:.1f}% と高パフォーマンス',
                'impact': f'予算2倍で月間 ¥{metrics["attributed_value"]:,.0f} の追加収益期待'
            })
    
    # 推奨事項を表示
    for rec in optimization_recommendations:
        type_colors = {
            'urgent': '#ef4444',
            'optimize': '#f59e0b',
            'scale': '#10b981'
        }
        
        type_icons = {
            'urgent': '🚨',
            'optimize': '⚡',
            'scale': '🚀'
        }
        
        color = type_colors[rec['type']]
        icon = type_icons[rec['type']]
        
        st.markdown(f"""
        <div class="insight-card" style="border-left: 4px solid {color};">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <span class="insight-title">{rec['touchpoint']} - {rec['action']}</span>
            </div>
            <div style="margin-bottom: 10px;">
                <strong>理由:</strong> {rec['reason']}<br>
                <strong>期待効果:</strong> {rec['impact']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # データ品質インジケーター
    st.markdown("#### 📊 データ品質インジケーター")
    
    # データ品質スコア計算
    data_completeness = 0.92  # サンプルデータの完全性
    data_accuracy = 0.88      # データの正確性
    sample_size_score = min(len(customer_journeys) / 1000, 1.0)  # サンプルサイズスコア
    time_range_score = 0.95   # 時間範囲の適切性
    
    overall_quality = (data_completeness + data_accuracy + sample_size_score + time_range_score) / 4
    
    quality_metrics = [
        ("データ完全性", data_completeness, "欠損データの少なさ"),
        ("データ精度", data_accuracy, "データの正確性と一貫性"),
        ("サンプルサイズ", sample_size_score, "統計的信頼性のためのサンプル数"),
        ("時間範囲", time_range_score, "分析に適した期間のデータ")
    ]
    
    for metric_name, score, description in quality_metrics:
        st.markdown(f"""
        <div class="data-quality">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong>{metric_name}</strong>
                <span style="color: #8b5cf6; font-weight: bold;">{score*100:.0f}%</span>
            </div>
            <div class="quality-score">
                <div class="quality-bar">
                    <div class="quality-fill" style="width: {score*100}%;"></div>
                </div>
            </div>
            <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 5px;">{description}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 総合品質スコア
    st.markdown(f"""
    <div class="significance-test">
        <div style="text-align: center;">
            <h4 style="color: #8b5cf6; margin-bottom: 15px;">総合データ品質スコア</h4>
            <div style="font-size: 3rem; font-weight: bold; color: #8b5cf6; margin-bottom: 10px;">
                {overall_quality*100:.0f}%
            </div>
            <div style="color: #94a3b8;">
                このスコアは分析結果の信頼性を示しています
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 統計的検定タブ
with tabs[3]:
    st.markdown("### 🔬 統計的有意性検定")
    
    # 検定設定
    col1, col2 = st.columns(2)
    
    with col1:
        test_model1 = st.selectbox("検定モデル1", list(attribution_results.keys()), key="test_model1")
    
    with col2:
        test_model2 = st.selectbox("検定モデル2", list(attribution_results.keys()), index=1, key="test_model2")
    
    if test_model1 != test_model2:
        # 統計的検定実行
        test_results = perform_statistical_significance_test(
            attribution_results[test_model1],
            attribution_results[test_model2]
        )
        
        # 検定結果表示
        st.markdown(f"#### 📊 {test_model1} vs {test_model2} 検定結果")
        
        significance_class = "significant" if test_results['significant'] else "not-significant"
        significance_text = "統計的に有意" if test_results['significant'] else "統計的に非有意"
        
        st.markdown(f"""
        <div class="significance-test">
            <div class="test-result">
                <div class="test-metric">
                    <div class="test-value">{test_results['p_value']:.4f}</div>
                    <div class="test-label">p値</div>
                </div>
                <div class="test-metric">
                    <div class="test-value">{test_results['test_statistic']:.2f}</div>
                    <div class="test-label">検定統計量</div>
                </div>
                <div class="test-metric">
                    <div class="test-value">{test_results['effect_size']:.2f}</div>
                    <div class="test-label">効果量</div>
                </div>
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <div class="significance-indicator {significance_class}">
                    {significance_text} (α = 0.05)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 信頼区間
        ci_lower, ci_upper = test_results['confidence_interval']
        
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">95% 信頼区間</div>
            <div style="text-align: center; margin: 15px 0;">
                <span style="font-size: 1.5rem; font-weight: bold; color: #8b5cf6;">
                    [{ci_lower:,.0f}, {ci_upper:,.0f}]
                </span>
            </div>
            <div style="color: #94a3b8;">
                真の差が95%の確率でこの範囲内に存在します
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 検定解釈
        interpretation = []
        
        if test_results['significant']:
            interpretation.append("✅ 2つのモデル間には統計的に有意な差があります")
            if test_results['effect_size'] > 0.8:
                interpretation.append("🔥 効果量が大きく、実用的に意味のある差です")
            elif test_results['effect_size'] > 0.5:
                interpretation.append("⚡ 効果量は中程度で、注目すべき差です")
            else:
                interpretation.append("📊 効果量は小さいですが、統計的には有意です")
        else:
            interpretation.append("❌ 2つのモデル間に統計的有意差は認められません")
            interpretation.append("🤔 より多くのデータが必要かもしれません")
        
        if test_results['p_value'] < 0.001:
            interpretation.append("⭐ 非常に強い証拠で差があることを示しています")
        elif test_results['p_value'] < 0.01:
            interpretation.append("💪 強い証拠で差があることを示しています")
        
        st.markdown("#### 💡 検定結果の解釈")
        
        for i, interp in enumerate(interpretation, 1):
            st.markdown(f"""
            <div class="insight-card">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="background: #8b5cf6; color: white; width: 25px; height: 25px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold;">{i}</span>
                    <span>{interp}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # パワー分析
        st.markdown("#### ⚡ パワー分析")
        
        # サンプルサイズの影響をシミュレーション
        sample_sizes = [50, 100, 200, 500, 1000]
        power_values = []
        
        for n in sample_sizes:
            # 簡易パワー計算（実際はより複雑）
            z_alpha = 1.96  # α = 0.05の臨界値
            effect_size = test_results['effect_size']
            power = 1 - stats.norm.cdf(z_alpha - effect_size * np.sqrt(n/2))
            power_values.append(max(0, min(1, power)))
        
        fig_power = px.line(
            x=sample_sizes,
            y=power_values,
            title="サンプルサイズと検定力の関係",
            labels={'x': 'サンプルサイズ', 'y': '検定力'},
            markers=True
        )
        
        fig_power.add_hline(y=0.8, line_dash="dash", line_color="rgba(255,255,255,0.5)", 
                           annotation_text="推奨検定力 0.8")
        
        fig_power.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_power, use_container_width=True)
    
    # 多重比較補正
    st.markdown("#### 🔢 多重比較補正")
    
    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">Bonferroni補正</div>
        <div style="margin: 15px 0;">
            複数のモデルを同時に比較する場合、第一種の過誤率を制御するため、
            有意水準を比較回数で割る必要があります。
        </div>
        <div style="text-align: center;">
            <span style="font-size: 1.2rem; color: #8b5cf6;">
                補正済み α = 0.05 / {len(attribution_results)} = {0.05/len(attribution_results):.4f}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 予測分析タブ  
with tabs[4]:
    st.markdown("### 🤖 予測分析・機械学習モデル")
    
    # 予測モデル設定
    col1, col2 = st.columns(2)
    
    with col1:
        prediction_target = st.selectbox(
            "予測対象",
            ["コンバージョン確率", "LTV予測", "最適予算配分", "チャーン予測"]
        )
    
    with col2:
        prediction_horizon = st.selectbox(
            "予測期間",
            ["1週間", "1ヶ月", "3ヶ月", "6ヶ月"]
        )
    
    # 予測モデル結果（シミュレーション）
    st.markdown("#### 🎯 予測モデル結果")
    
    if prediction_target == "コンバージョン確率":
        # コンバージョン確率予測
        touchpoint_conversion_probs = {}
        for tp in touchpoint_costs.keys():
            base_prob = np.random.uniform(0.02, 0.15)
            touchpoint_conversion_probs[tp] = base_prob
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 タッチポイント別コンバージョン確率")
            
            sorted_probs = sorted(touchpoint_conversion_probs.items(), key=lambda x: x[1], reverse=True)
            
            for i, (touchpoint, prob) in enumerate(sorted_probs, 1):
                confidence = np.random.uniform(0.75, 0.95)
                
                st.markdown(f"""
                <div class="prediction-model">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h5 style="color: #8b5cf6; margin-bottom: 5px;">{touchpoint}</h5>
                            <div style="font-size: 1.5rem; font-weight: bold; color: #10b981;">
                                {prob*100:.1f}%
                            </div>
                        </div>
                        <div class="prediction-confidence">
                            <div class="confidence-circle">
                                {confidence*100:.0f}%
                            </div>
                            <div style="color: #94a3b8; font-size: 0.8rem;">信頼度</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # 予測精度グラフ
            days = list(range(1, 31))
            actual = np.random.uniform(0.03, 0.12, 30)
            predicted = actual + np.random.normal(0, 0.01, 30)
            
            fig_accuracy = go.Figure()
            
            fig_accuracy.add_trace(go.Scatter(
                x=days,
                y=actual,
                mode='lines+markers',
                name='実際のコンバージョン率',
                line=dict(color='#10b981', width=2)
            ))
            
            fig_accuracy.add_trace(go.Scatter(
                x=days,
                y=predicted,
                mode='lines+markers',
                name='予測コンバージョン率',
                line=dict(color='#8b5cf6', width=2, dash='dash')
            ))
            
            fig_accuracy.update_layout(
                title="予測精度検証",
                xaxis_title="日数",
                yaxis_title="コンバージョン率",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_accuracy, use_container_width=True)
    
    elif prediction_target == "最適予算配分":
        # 最適予算配分
        st.markdown("##### 💰 AI推奨予算配分")
        
        total_budget = 100000  # 仮想総予算
        
        # 現在の配分
        current_allocation = {tp: cost for tp, cost in touchpoint_costs.items() if cost > 0}
        current_total = sum(current_allocation.values())
        current_percentages = {tp: (cost/current_total)*100 for tp, cost in current_allocation.items()}
        
        # AI推奨配分（ROIベース）
        roi_scores = {tp: roi_metrics[selected_model].get(tp, {}).get('roi', 0) for tp in current_allocation.keys()}
        positive_roi_tps = {tp: max(0, roi) for tp, roi in roi_scores.items()}
        total_roi_score = sum(positive_roi_tps.values())
        
        if total_roi_score > 0:
            ai_allocation = {tp: (score/total_roi_score)*total_budget for tp, score in positive_roi_tps.items()}
        else:
            ai_allocation = current_allocation
        
        ai_percentages = {tp: (alloc/total_budget)*100 for tp, alloc in ai_allocation.items()}
        
        # 比較表示
        allocation_comparison = []
        for tp in current_allocation.keys():
            current_pct = current_percentages.get(tp, 0)
            ai_pct = ai_percentages.get(tp, 0)
            change = ai_pct - current_pct
            
            allocation_comparison.append({
                'touchpoint': tp,
                'current': current_pct,
                'ai_recommended': ai_pct,
                'change': change
            })
        
        allocation_df = pd.DataFrame(allocation_comparison)
        
        fig_allocation = go.Figure()
        
        fig_allocation.add_trace(go.Bar(
            name='現在の配分',
            x=allocation_df['touchpoint'],
            y=allocation_df['current'],
            marker_color='rgba(239, 68, 68, 0.8)'
        ))
        
        fig_allocation.add_trace(go.Bar(
            name='AI推奨配分',
            x=allocation_df['touchpoint'],
            y=allocation_df['ai_recommended'],
            marker_color='rgba(139, 92, 246, 0.8)'
        ))
        
        fig_allocation.update_layout(
            title="予算配分比較",
            xaxis_title="タッチポイント",
            yaxis_title="予算配分 (%)",
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_allocation, use_container_width=True)
        
        # 配分変更インパクト
        st.markdown("##### 📈 配分変更による期待インパクト")
        
        total_current_roi = sum(roi_metrics[selected_model].get(tp, {}).get('roi', 0) * current_percentages.get(tp, 0)/100 for tp in current_allocation.keys())
        total_ai_roi = sum(roi_metrics[selected_model].get(tp, {}).get('roi', 0) * ai_percentages.get(tp, 0)/100 for tp in current_allocation.keys())
        
        roi_improvement = total_ai_roi - total_current_roi
        
        st.markdown(f"""
        <div class="significance-test">
            <div style="text-align: center;">
                <h4 style="color: #8b5cf6; margin-bottom: 15px;">予想ROI改善</h4>
                <div style="font-size: 3rem; font-weight: bold; color: #10b981; margin-bottom: 10px;">
                    +{roi_improvement:.1f}%
                </div>
                <div style="color: #94a3b8;">
                    AI推奨配分により期待される追加収益率
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # モデル性能指標
    st.markdown("#### 📊 モデル性能指標")
    
    performance_metrics = [
        {"metric": "精度 (Accuracy)", "value": 0.847, "benchmark": 0.800},
        {"metric": "適合率 (Precision)", "value": 0.823, "benchmark": 0.750},
        {"metric": "再現率 (Recall)", "value": 0.789, "benchmark": 0.700},
        {"metric": "F1スコア", "value": 0.806, "benchmark": 0.725},
        {"metric": "AUC-ROC", "value": 0.912, "benchmark": 0.850}
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        for metric in performance_metrics[:3]:
            performance_class = "roi-positive" if metric['value'] > metric['benchmark'] else "roi-negative"
            
            st.markdown(f"""
            <div class="roi-metric">
                <div class="roi-value">{metric['value']:.3f}</div>
                <div class="roi-label">{metric['metric']}</div>
                <div class="roi-change {performance_class}">
                    ベンチマーク: {metric['benchmark']:.3f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        for metric in performance_metrics[3:]:
            performance_class = "roi-positive" if metric['value'] > metric['benchmark'] else "roi-negative"
            
            st.markdown(f"""
            <div class="roi-metric">
                <div class="roi-value">{metric['value']:.3f}</div>
                <div class="roi-label">{metric['metric']}</div>
                <div class="roi-change {performance_class}">
                    ベンチマーク: {metric['benchmark']:.3f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 特徴量重要度
    st.markdown("#### 🎯 特徴量重要度")
    
    feature_importance = {
        "タッチポイント順序": 0.234,
        "チャネル組み合わせ": 0.198,
        "接触間隔": 0.167,
        "デバイスタイプ": 0.143,
        "時間帯": 0.089,
        "季節要因": 0.076,
        "広告費用": 0.058,
        "競合活動": 0.035
    }
    
    fig_importance = px.bar(
        x=list(feature_importance.values()),
        y=list(feature_importance.keys()),
        orientation='h',
        title="モデル特徴量重要度",
        color=list(feature_importance.values()),
        color_continuous_scale="Viridis"
    )
    
    fig_importance.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_title="重要度",
        yaxis_title="特徴量"
    )
    
    st.plotly_chart(fig_importance, use_container_width=True)

# サイドバー
with st.sidebar:
    st.header("🎯 アトリビューション分析")
    
    # 分析設定
    st.subheader("⚙️ 分析設定")
    
    analysis_period = st.selectbox(
        "分析期間",
        ["過去7日", "過去30日", "過去90日", "カスタム"]
    )
    
    attribution_window = st.slider(
        "アトリビューション窓 (日)",
        1, 30, 14
    )
    
    confidence_level = st.selectbox(
        "信頼水準",
        ["90%", "95%", "99%"],
        index=1
    )
    
    st.markdown("---")
    
    # データ概要
    st.subheader("📊 データ概要")
    
    st.metric("総ジャーニー数", len(customer_journeys))
    st.metric("コンバージョン数", total_conversions)
    st.metric("平均タッチポイント数", f"{avg_touchpoints:.1f}")
    
    conversion_rate = (total_conversions / len(customer_journeys) * 100) if customer_journeys else 0
    st.metric("コンバージョン率", f"{conversion_rate:.1f}%")
    
    st.markdown("---")
    
    # モデル比較
    st.subheader("🔍 モデル比較")
    
    model_total_values = {}
    for model, attributions in attribution_results.items():
        model_total_values[model] = sum(attributions.values())
    
    sorted_models = sorted(model_total_values.items(), key=lambda x: x[1], reverse=True)
    
    for i, (model, total_value) in enumerate(sorted_models, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}位"
        st.markdown(f"{medal} {model}")
        st.caption(f"¥{total_value:,.0f}")
    
    st.markdown("---")
    
    # アラート
    st.subheader("🚨 アラート")
    
    alerts = [
        {"type": "warning", "message": "Display Adの効率低下", "time": "10分前"},
        {"type": "info", "message": "Organic Search貢献度上昇", "time": "1時間前"},
        {"type": "success", "message": "モデル精度向上", "time": "3時間前"}
    ]
    
    for alert in alerts:
        alert_icon = {"warning": "⚠️", "info": "ℹ️", "success": "✅"}[alert['type']]
        st.markdown(f"{alert_icon} {alert['message']}")
        st.caption(alert['time'])
    
    st.markdown("---")
    
    # エクスポート
    st.subheader("📥 エクスポート")
    
    if st.button("📊 レポート生成", use_container_width=True):
        st.success("📈 アトリビューション分析レポートを生成中...")
    
    if st.button("💾 データエクスポート", use_container_width=True):
        export_data = {
            "attribution_results": attribution_results,
            "roi_metrics": roi_metrics,
            "customer_journeys": len(customer_journeys),
            "export_timestamp": datetime.now().isoformat()
        }
        
        st.download_button(
            "📥 JSONダウンロード",
            data=json.dumps(export_data, ensure_ascii=False, indent=2),
            file_name=f"attribution_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("pages/../home.py")
    
    if st.button("🌐 マルチプラットフォーム", use_container_width=True):
        st.switch_page("pages/multi_platform_manager.py")
    
    if st.button("⚡ リアルタイム最適化", use_container_width=True):
        st.switch_page("pages/realtime_ad_optimizer.py")

# フッター
st.markdown("---")
st.caption("🎯 Attribution Analysis: 最先端のマルチタッチアトリビューション分析で、真のROIを解明し、マーケティング投資を最適化します。")