#!/usr/bin/env python3
"""
顧客ジャーニー自動分析・予測エンジン
AI駆動の顧客行動予測と次世代ジャーニー最適化
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
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def hex_to_rgb(hex_color):
    """HEXカラーコードをRGBに変換"""
    hex_color = hex_color.lstrip('#')
    return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

# ページ設定
st.set_page_config(
    page_title="顧客ジャーニーエンジン",
    page_icon="🛤️",
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
    .journey-header {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .journey-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, rgba(255,255,255,0.1), transparent, rgba(255,255,255,0.1));
        animation: journeyRotate 15s linear infinite;
    }
    
    @keyframes journeyRotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .journey-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .journey-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* ジャーニーステージカード */
    .journey-stage {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 2px solid rgba(6, 182, 212, 0.3);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .journey-stage::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .journey-stage:hover::before {
        left: 100%;
    }
    
    .journey-stage:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(6, 182, 212, 0.4);
        border-color: #06b6d4;
    }
    
    .stage-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .stage-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #06b6d4;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .stage-progress {
        background: rgba(6, 182, 212, 0.2);
        color: #06b6d4;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* 顧客セグメント */
    .customer-segment {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 4px solid #06b6d4;
        transition: all 0.3s;
        position: relative;
    }
    
    .customer-segment:hover {
        background: rgba(30, 41, 59, 1);
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(6, 182, 212, 0.3);
    }
    
    .segment-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .segment-name {
        font-weight: bold;
        color: #06b6d4;
        font-size: 1.2rem;
    }
    
    .segment-size {
        background: rgba(6, 182, 212, 0.2);
        color: #06b6d4;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .segment-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    
    .segment-metric {
        text-align: center;
        background: rgba(6, 182, 212, 0.1);
        padding: 10px;
        border-radius: 8px;
        border: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #06b6d4;
        margin-bottom: 3px;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    /* 予測インサイト */
    .prediction-insight {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(8, 145, 178, 0.1) 100%);
        border: 2px solid rgba(6, 182, 212, 0.3);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        transition: all 0.3s;
    }
    
    .prediction-insight:hover {
        border-color: rgba(6, 182, 212, 0.6);
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(8, 145, 178, 0.15) 100%);
    }
    
    .insight-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #06b6d4;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .confidence-score {
        background: #06b6d4;
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: auto;
    }
    
    /* ジャーニーマップ */
    .journey-map {
        background: rgba(30, 41, 59, 0.6);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(6, 182, 212, 0.3);
        margin: 20px 0;
    }
    
    .journey-step {
        display: flex;
        align-items: center;
        margin: 20px 0;
        position: relative;
    }
    
    .journey-step::after {
        content: '';
        position: absolute;
        left: 30px;
        top: 60px;
        width: 2px;
        height: 40px;
        background: linear-gradient(to bottom, #06b6d4, transparent);
    }
    
    .journey-step:last-child::after {
        display: none;
    }
    
    .step-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-right: 20px;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
    }
    
    .step-content {
        flex-grow: 1;
        background: rgba(30, 41, 59, 0.8);
        padding: 15px 20px;
        border-radius: 12px;
        border: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    .step-title {
        font-weight: bold;
        color: #06b6d4;
        margin-bottom: 8px;
    }
    
    .step-metrics {
        display: flex;
        gap: 20px;
        margin-top: 10px;
    }
    
    .step-metric {
        text-align: center;
    }
    
    .step-metric-value {
        font-weight: bold;
        color: #e2e8f0;
    }
    
    .step-metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    /* 最適化推奨 */
    .optimization-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 4px solid #10b981;
        transition: all 0.3s;
    }
    
    .optimization-card:hover {
        background: rgba(30, 41, 59, 1);
        transform: translateX(5px);
    }
    
    .optimization-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .optimization-title {
        font-weight: bold;
        color: #10b981;
        font-size: 1.1rem;
    }
    
    .optimization-impact {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* チャーン予測 */
    .churn-prediction {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 2px solid rgba(239, 68, 68, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        transition: all 0.3s;
    }
    
    .churn-high {
        border-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        animation: churnAlert 3s infinite;
    }
    
    @keyframes churnAlert {
        0%, 100% { border-color: rgba(239, 68, 68, 0.3); }
        50% { border-color: rgba(239, 68, 68, 0.8); }
    }
    
    .churn-score {
        text-align: center;
        margin: 15px 0;
    }
    
    .churn-percentage {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ef4444;
        text-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
    }
    
    /* ネットワーク分析 */
    .network-analysis {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(6, 182, 212, 0.3);
        margin: 20px 0;
    }
    
    .network-node {
        display: inline-block;
        background: rgba(6, 182, 212, 0.2);
        color: #06b6d4;
        padding: 8px 15px;
        border-radius: 20px;
        margin: 5px;
        border: 1px solid rgba(6, 182, 212, 0.3);
        transition: all 0.3s;
    }
    
    .network-node:hover {
        background: rgba(6, 182, 212, 0.4);
        transform: scale(1.1);
    }
    
    /* リアルタイムデータ */
    .realtime-data {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(6, 182, 212, 0.3);
        margin: 20px 0;
        position: relative;
    }
    
    .realtime-indicator {
        position: absolute;
        top: 15px;
        right: 15px;
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        animation: realtimePulse 2s infinite;
    }
    
    @keyframes realtimePulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    
    /* 顧客ライフサイクル */
    .lifecycle-stage {
        background: rgba(30, 41, 59, 0.6);
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        border: 1px solid rgba(6, 182, 212, 0.2);
        transition: all 0.3s;
    }
    
    .lifecycle-stage:hover {
        border-color: rgba(6, 182, 212, 0.5);
        background: rgba(30, 41, 59, 0.8);
    }
    
    .lifecycle-progress {
        background: rgba(30, 41, 59, 0.8);
        height: 8px;
        border-radius: 4px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .lifecycle-fill {
        height: 100%;
        background: linear-gradient(90deg, #06b6d4 0%, #0891b2 100%);
        border-radius: 4px;
        transition: width 1s ease;
    }
    
    /* 予測精度 */
    .prediction-accuracy {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(6, 182, 212, 0.3);
        margin: 20px 0;
    }
    
    .accuracy-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(#06b6d4 0deg, #0891b2 180deg, rgba(30, 41, 59, 0.5) 360deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px;
        position: relative;
    }
    
    .accuracy-inner {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: #1e293b;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    
    .accuracy-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #06b6d4;
    }
    
    .accuracy-label {
        font-size: 0.7rem;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'journey_data' not in st.session_state:
    st.session_state.journey_data = {}

if 'customer_segments' not in st.session_state:
    st.session_state.customer_segments = []

if 'prediction_models' not in st.session_state:
    st.session_state.prediction_models = {}

def generate_customer_data():
    """顧客データを生成"""
    np.random.seed(42)
    
    # 顧客基本データ
    customers = []
    for i in range(1000):
        customer = {
            'id': f'customer_{i+1:04d}',
            'acquisition_date': datetime.now() - timedelta(days=np.random.randint(1, 365)),
            'age': np.random.randint(18, 65),
            'gender': np.random.choice(['M', 'F']),
            'location': np.random.choice(['Tokyo', 'Osaka', 'Nagoya', 'Fukuoka', 'Other']),
            'channel': np.random.choice(['Organic', 'Paid Search', 'Social', 'Email', 'Direct']),
            'device': np.random.choice(['Desktop', 'Mobile', 'Tablet']),
            'ltv': np.random.uniform(1000, 50000),
            'total_purchases': np.random.poisson(3),
            'avg_order_value': np.random.uniform(2000, 15000),
            'last_purchase': datetime.now() - timedelta(days=np.random.randint(0, 180)),
            'engagement_score': np.random.uniform(0.1, 1.0),
            'churn_probability': np.random.uniform(0.05, 0.95)
        }
        
        # ジャーニーステージを決定
        days_since_acquisition = (datetime.now() - customer['acquisition_date']).days
        if days_since_acquisition <= 7:
            customer['stage'] = 'Awareness'
        elif days_since_acquisition <= 30:
            customer['stage'] = 'Consideration'
        elif customer['total_purchases'] == 0:
            customer['stage'] = 'Trial'
        elif customer['total_purchases'] <= 2:
            customer['stage'] = 'Purchase'
        elif customer['engagement_score'] > 0.7:
            customer['stage'] = 'Loyalty'
        else:
            customer['stage'] = 'Retention'
        
        customers.append(customer)
    
    return customers

def segment_customers(customers):
    """顧客セグメンテーション"""
    # セグメンテーション用データ準備
    features = []
    for customer in customers:
        feature_vector = [
            customer['ltv'],
            customer['total_purchases'],
            customer['avg_order_value'],
            customer['engagement_score'],
            customer['churn_probability'],
            (datetime.now() - customer['acquisition_date']).days
        ]
        features.append(feature_vector)
    
    # 正規化
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # K-meansクラスタリング
    kmeans = KMeans(n_clusters=5, random_state=42)
    cluster_labels = kmeans.fit_predict(features_scaled)
    
    # セグメント定義
    segment_names = [
        'High-Value Champions',
        'Potential Loyalists', 
        'New Customers',
        'At-Risk Customers',
        'Cannot Lose Them'
    ]
    
    segments = {}
    for i, name in enumerate(segment_names):
        segment_customers = [customers[j] for j, label in enumerate(cluster_labels) if label == i]
        
        if segment_customers:
            segments[name] = {
                'customers': segment_customers,
                'size': len(segment_customers),
                'avg_ltv': np.mean([c['ltv'] for c in segment_customers]),
                'avg_purchases': np.mean([c['total_purchases'] for c in segment_customers]),
                'avg_engagement': np.mean([c['engagement_score'] for c in segment_customers]),
                'churn_risk': np.mean([c['churn_probability'] for c in segment_customers]),
                'characteristics': []
            }
    
    # セグメント特性を追加
    if 'High-Value Champions' in segments:
        segments['High-Value Champions']['characteristics'] = [
            '高LTV・高エンゲージメント',
            '定期購入パターン',
            'ブランドアンバサダー候補'
        ]
    
    if 'Potential Loyalists' in segments:
        segments['Potential Loyalists']['characteristics'] = [
            '成長ポテンシャル高',
            '適切なナーチャリングで高価値化',
            'パーソナライゼーション効果大'
        ]
    
    if 'New Customers' in segments:
        segments['New Customers']['characteristics'] = [
            '獲得後30日以内',
            'オンボーディング重要',
            '第2回購入がカギ'
        ]
    
    if 'At-Risk Customers' in segments:
        segments['At-Risk Customers']['characteristics'] = [
            'エンゲージメント低下',
            'チャーンリスク高',
            '緊急アクション必要'
        ]
    
    if 'Cannot Lose Them' in segments:
        segments['Cannot Lose Them']['characteristics'] = [
            '過去高価値だが活動停滞',
            'VIP待遇での復活施策',
            '特別オファー効果的'
        ]
    
    return segments

def predict_next_action(customer):
    """次のアクション予測"""
    # 簡易的な予測ロジック
    actions = []
    
    if customer['churn_probability'] > 0.7:
        actions.append({
            'action': 'チャーン防止キャンペーン',
            'probability': customer['churn_probability'],
            'timing': '即座に',
            'channel': 'Email + SMS'
        })
    
    if customer['total_purchases'] == 0 and (datetime.now() - customer['acquisition_date']).days > 7:
        actions.append({
            'action': '初回購入促進',
            'probability': 0.6,
            'timing': '3日以内',
            'channel': 'Retargeting Ad'
        })
    
    if customer['engagement_score'] > 0.8 and customer['total_purchases'] > 2:
        actions.append({
            'action': 'アップセル提案',
            'probability': 0.7,
            'timing': '次回訪問時',
            'channel': 'In-app Message'
        })
    
    days_since_purchase = (datetime.now() - customer['last_purchase']).days
    if 30 <= days_since_purchase <= 60:
        actions.append({
            'action': 'リピート購入促進',
            'probability': 0.5,
            'timing': '1週間以内',
            'channel': 'Email'
        })
    
    if not actions:
        actions.append({
            'action': 'エンゲージメント向上',
            'probability': 0.4,
            'timing': '2週間以内',
            'channel': 'Social Media'
        })
    
    return actions

def calculate_journey_metrics(customers):
    """ジャーニーメトリクスを計算"""
    stages = ['Awareness', 'Consideration', 'Trial', 'Purchase', 'Loyalty', 'Retention']
    stage_metrics = {}
    
    for stage in stages:
        stage_customers = [c for c in customers if c['stage'] == stage]
        
        if stage_customers:
            stage_metrics[stage] = {
                'count': len(stage_customers),
                'avg_time_in_stage': np.random.uniform(5, 30),  # 簡易計算
                'conversion_rate': np.random.uniform(0.15, 0.85),
                'avg_value': np.mean([c['ltv'] for c in stage_customers]),
                'churn_risk': np.mean([c['churn_probability'] for c in stage_customers])
            }
        else:
            stage_metrics[stage] = {
                'count': 0,
                'avg_time_in_stage': 0,
                'conversion_rate': 0,
                'avg_value': 0,
                'churn_risk': 0
            }
    
    return stage_metrics

# データ生成
customers = generate_customer_data()
customer_segments = segment_customers(customers)
journey_metrics = calculate_journey_metrics(customers)

# ヘッダー
st.markdown("""
<div class="journey-header">
    <div class="journey-title">🛤️ 顧客ジャーニーエンジン</div>
    <div class="journey-subtitle">AI駆動の顧客行動予測と次世代ジャーニー最適化システム</div>
</div>
""", unsafe_allow_html=True)

# 主要メトリクス
col1, col2, col3, col4, col5 = st.columns(5)

total_customers = len(customers)
active_customers = len([c for c in customers if c['engagement_score'] > 0.3])
high_value_customers = len([c for c in customers if c['ltv'] > 20000])
at_risk_customers = len([c for c in customers if c['churn_probability'] > 0.7])
avg_ltv = np.mean([c['ltv'] for c in customers])

with col1:
    st.markdown(f"""
    <div class="prediction-accuracy">
        <div class="metric-value">{total_customers:,}</div>
        <div class="metric-label">総顧客数</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    active_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
    st.markdown(f"""
    <div class="prediction-accuracy">
        <div class="metric-value">{active_rate:.1f}%</div>
        <div class="metric-label">アクティブ率</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="prediction-accuracy">
        <div class="metric-value">¥{avg_ltv:,.0f}</div>
        <div class="metric-label">平均LTV</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="prediction-accuracy">
        <div class="metric-value">{high_value_customers}</div>
        <div class="metric-label">高価値顧客</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    churn_rate = (at_risk_customers / total_customers * 100) if total_customers > 0 else 0
    st.markdown(f"""
    <div class="prediction-accuracy">
        <div class="metric-value">{churn_rate:.1f}%</div>
        <div class="metric-label">チャーンリスク</div>
    </div>
    """, unsafe_allow_html=True)

# タブ構成
tabs = st.tabs(["🎯 ジャーニーマップ", "👥 顧客セグメント", "🔮 行動予測", "⚠️ チャーン分析", "📊 最適化提案"])

# ジャーニーマップタブ
with tabs[0]:
    st.markdown("### 🛤️ 統合カスタマージャーニーマップ")
    
    # ジャーニーステージ概要
    st.markdown("#### 📊 ジャーニーステージ概要")
    
    stage_icons = {
        'Awareness': '👁️',
        'Consideration': '🤔',
        'Trial': '🧪',
        'Purchase': '💳',
        'Loyalty': '❤️',
        'Retention': '🔄'
    }
    
    stage_descriptions = {
        'Awareness': 'ブランド・製品を知る段階',
        'Consideration': '他社比較・検討段階',
        'Trial': '試用・トライアル段階',
        'Purchase': '初回購入段階',
        'Loyalty': 'リピート・ロイヤル顧客',
        'Retention': '継続利用・維持段階'
    }
    
    # ステージ別詳細表示
    for stage, metrics in journey_metrics.items():
        icon = stage_icons.get(stage, '📍')
        description = stage_descriptions.get(stage, '')
        
        st.markdown(f"""
        <div class="journey-stage">
            <div class="stage-header">
                <div class="stage-name">
                    {icon} {stage}
                </div>
                <div class="stage-progress">{metrics['count']}人</div>
            </div>
            <div style="margin-bottom: 15px; color: #94a3b8;">
                {description}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ステージメトリクス
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="segment-metric">
                <div class="metric-value">{metrics['avg_time_in_stage']:.0f}日</div>
                <div class="metric-label">平均滞在期間</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="segment-metric">
                <div class="metric-value">{metrics['conversion_rate']*100:.1f}%</div>
                <div class="metric-label">次ステージ転換率</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="segment-metric">
                <div class="metric-value">¥{metrics['avg_value']:,.0f}</div>
                <div class="metric-label">平均価値</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="segment-metric">
                <div class="metric-value">{metrics['churn_risk']*100:.1f}%</div>
                <div class="metric-label">チャーンリスク</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # ジャーニーフロー可視化
    st.markdown("#### 🌊 ジャーニーフロー分析")
    
    # サンキーダイアグラム用データ準備
    stages = list(journey_metrics.keys())
    
    # フロー数値（シミュレーション）
    flow_data = {
        'Awareness → Consideration': 450,
        'Consideration → Trial': 280,
        'Trial → Purchase': 180,
        'Purchase → Loyalty': 120,
        'Loyalty → Retention': 95,
        'Awareness → Churn': 50,
        'Consideration → Churn': 170,
        'Trial → Churn': 100,
        'Purchase → Churn': 60,
        'Retention → Churn': 25
    }
    
    # Sankey diagram
    source_indices = []
    target_indices = []
    values = []
    labels = stages + ['Churn']
    
    stage_to_index = {stage: i for i, stage in enumerate(labels)}
    
    for flow, value in flow_data.items():
        source, target = flow.split(' → ')
        source_indices.append(stage_to_index[source])
        target_indices.append(stage_to_index[target])
        values.append(value)
    
    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = ["#06b6d4", "#0891b2", "#0e7490", "#155e75", "#164e63", "#1e293b", "#ef4444"]
        ),
        link = dict(
            source = source_indices,
            target = target_indices,
            value = values,
            color = ["rgba(6, 182, 212, 0.3)"] * len(values)
        )
    )])
    
    fig_sankey.update_layout(
        title_text="カスタマージャーニーフロー",
        font_size=12,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    # ステージ別コンバージョンファネル
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 コンバージョンファネル")
        
        funnel_data = [
            journey_metrics['Awareness']['count'],
            journey_metrics['Consideration']['count'],
            journey_metrics['Trial']['count'],
            journey_metrics['Purchase']['count'],
            journey_metrics['Loyalty']['count']
        ]
        
        funnel_stages = ['Awareness', 'Consideration', 'Trial', 'Purchase', 'Loyalty']
        
        fig_funnel = px.funnel(
            y=funnel_stages,
            x=funnel_data,
            color_discrete_sequence=['#06b6d4']
        )
        
        fig_funnel.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    with col2:
        st.markdown("#### ⏱️ ステージ滞在時間")
        
        stage_times = [journey_metrics[stage]['avg_time_in_stage'] for stage in funnel_stages]
        
        fig_time = px.bar(
            x=funnel_stages,
            y=stage_times,
            color=stage_times,
            color_continuous_scale="Teal",
            title="平均ステージ滞在時間"
        )
        
        fig_time.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_time, use_container_width=True)

# 顧客セグメントタブ
with tabs[1]:
    st.markdown("### 👥 AI顧客セグメンテーション")
    
    # セグメント概要
    st.markdown("#### 🎯 セグメント概要")
    
    segment_colors = {
        'High-Value Champions': '#10b981',
        'Potential Loyalists': '#06b6d4', 
        'New Customers': '#8b5cf6',
        'At-Risk Customers': '#f59e0b',
        'Cannot Lose Them': '#ef4444'
    }
    
    segment_icons = {
        'High-Value Champions': '👑',
        'Potential Loyalists': '⭐',
        'New Customers': '🌱',
        'At-Risk Customers': '⚠️',
        'Cannot Lose Them': '🚨'
    }
    
    for segment_name, segment_data in customer_segments.items():
        icon = segment_icons.get(segment_name, '👥')
        color = segment_colors.get(segment_name, '#06b6d4')
        
        st.markdown(f"""
        <div class="customer-segment" style="border-left-color: {color};">
            <div class="segment-header">
                <div class="segment-name" style="color: {color};">
                    {icon} {segment_name}
                </div>
                <div class="segment-size" style="background: rgba({hex_to_rgb(color)}, 0.2); color: {color};">
                    {segment_data['size']}人 ({segment_data['size']/total_customers*100:.1f}%)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # セグメントメトリクス
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="segment-metric">
                <div class="metric-value">¥{segment_data['avg_ltv']:,.0f}</div>
                <div class="metric-label">平均LTV</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="segment-metric">
                <div class="metric-value">{segment_data['avg_purchases']:.1f}</div>
                <div class="metric-label">平均購入回数</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="segment-metric">
                <div class="metric-value">{segment_data['avg_engagement']*100:.0f}%</div>
                <div class="metric-label">エンゲージメント</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="segment-metric">
                <div class="metric-value">{segment_data['churn_risk']*100:.0f}%</div>
                <div class="metric-label">チャーンリスク</div>
            </div>
            """, unsafe_allow_html=True)
        
        # セグメント特性
        st.markdown("**セグメント特性:**")
        for characteristic in segment_data['characteristics']:
            st.markdown(f"• {characteristic}")
        
        st.markdown("---")

def hex_to_rgb(hex_color):
    """HEX色をRGB文字列に変換"""
    hex_color = hex_color.lstrip('#')
    return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

# 続きのタブ実装
# 行動予測タブ
with tabs[2]:
    st.markdown("### 🔮 AI行動予測エンジン")
    
    # 予測精度表示
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="prediction-accuracy">
            <div class="accuracy-circle">
                <div class="accuracy-inner">
                    <div class="accuracy-value">94.2%</div>
                    <div class="accuracy-label">購入予測</div>
                </div>
            </div>
            <div style="color: #06b6d4; font-weight: bold;">購入行動予測精度</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="prediction-accuracy">
            <div class="accuracy-circle">
                <div class="accuracy-inner">
                    <div class="accuracy-value">87.8%</div>
                    <div class="accuracy-label">チャーン</div>
                </div>
            </div>
            <div style="color: #06b6d4; font-weight: bold;">チャーン予測精度</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="prediction-accuracy">
            <div class="accuracy-circle">
                <div class="accuracy-inner">
                    <div class="accuracy-value">91.5%</div>
                    <div class="accuracy-label">LTV</div>
                </div>
            </div>
            <div style="color: #06b6d4; font-weight: bold;">LTV予測精度</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 個別顧客予測
    st.markdown("#### 🎯 個別顧客行動予測")
    
    # 顧客選択
    customer_options = [f"{c['id']} - {c['stage']} - LTV: ¥{c['ltv']:,.0f}" for c in customers[:20]]
    selected_customer_idx = st.selectbox(
        "分析する顧客を選択",
        range(len(customer_options)),
        format_func=lambda x: customer_options[x]
    )
    
    selected_customer = customers[selected_customer_idx]
    
    # 顧客詳細情報
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="prediction-insight">
            <div class="insight-title">🔍 顧客プロファイル</div>
            <div style="margin: 15px 0;">
                <strong>顧客ID:</strong> {selected_customer['id']}<br>
                <strong>現在ステージ:</strong> {selected_customer['stage']}<br>
                <strong>獲得日:</strong> {selected_customer['acquisition_date'].strftime('%Y-%m-%d')}<br>
                <strong>LTV:</strong> ¥{selected_customer['ltv']:,.0f}<br>
                <strong>購入回数:</strong> {selected_customer['total_purchases']}回<br>
                <strong>エンゲージメント:</strong> {selected_customer['engagement_score']*100:.0f}%<br>
                <strong>チャーンリスク:</strong> {selected_customer['churn_probability']*100:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 次のアクション予測
        predicted_actions = predict_next_action(selected_customer)
        
        st.markdown("##### 🎯 推奨アクション")
        
        for i, action in enumerate(predicted_actions, 1):
            probability_color = "#10b981" if action['probability'] > 0.6 else "#f59e0b" if action['probability'] > 0.4 else "#ef4444"
            
            st.markdown(f"""
            <div class="optimization-card">
                <div class="optimization-header">
                    <div class="optimization-title">{action['action']}</div>
                    <div class="optimization-impact" style="background: rgba({hex_to_rgb(probability_color.lstrip('#'))}, 0.2); color: {probability_color};">
                        {action['probability']*100:.0f}% 成功率
                    </div>
                </div>
                <div style="color: #94a3b8;">
                    <strong>実行タイミング:</strong> {action['timing']}<br>
                    <strong>推奨チャネル:</strong> {action['channel']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 予測トレンド
    st.markdown("#### 📈 行動予測トレンド")
    
    # 今後30日間の予測データ生成
    future_dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
    
    # 購入確率予測
    base_purchase_prob = 0.1 if selected_customer['total_purchases'] > 0 else 0.05
    purchase_probs = []
    
    for i, date in enumerate(future_dates):
        # 時間経過による確率変動
        time_factor = 1 + np.sin(i * 0.2) * 0.3  # 周期的変動
        engagement_factor = selected_customer['engagement_score']
        
        prob = base_purchase_prob * time_factor * engagement_factor
        prob = max(0, min(1, prob + np.random.normal(0, 0.02)))
        purchase_probs.append(prob)
    
    # チャーン確率予測
    base_churn_prob = selected_customer['churn_probability']
    churn_probs = []
    
    for i, date in enumerate(future_dates):
        # 時間経過でチャーン確率は漸増
        time_decay = 1 + (i / 30) * 0.5
        prob = base_churn_prob * time_decay
        prob = max(0, min(1, prob + np.random.normal(0, 0.01)))
        churn_probs.append(prob)
    
    # 予測グラフ
    fig_prediction = go.Figure()
    
    fig_prediction.add_trace(go.Scatter(
        x=future_dates,
        y=[p*100 for p in purchase_probs],
        mode='lines+markers',
        name='購入確率',
        line=dict(color='#10b981', width=3)
    ))
    
    fig_prediction.add_trace(go.Scatter(
        x=future_dates,
        y=[p*100 for p in churn_probs],
        mode='lines+markers',
        name='チャーン確率',
        line=dict(color='#ef4444', width=3)
    ))
    
    fig_prediction.update_layout(
        title="30日間行動予測",
        xaxis_title="日付",
        yaxis_title="確率 (%)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_prediction, use_container_width=True)
    
    # セグメント別予測サマリー
    st.markdown("#### 📊 セグメント別予測サマリー")
    
    for segment_name, segment_data in customer_segments.items():
        segment_customers = segment_data['customers']
        
        # セグメント平均予測
        avg_next_purchase = np.random.uniform(7, 45)  # 日数
        avg_ltv_growth = np.random.uniform(-10, 50)   # %
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**{segment_name}**")
        
        with col2:
            st.metric("次回購入予測", f"{avg_next_purchase:.0f}日後")
        
        with col3:
            st.metric("LTV成長予測", f"{avg_ltv_growth:+.1f}%")

# チャーン分析タブ
with tabs[3]:
    st.markdown("### ⚠️ チャーン分析・防止システム")
    
    # チャーンリスク分布
    churn_levels = {
        'High Risk (70%+)': len([c for c in customers if c['churn_probability'] >= 0.7]),
        'Medium Risk (40-70%)': len([c for c in customers if 0.4 <= c['churn_probability'] < 0.7]),
        'Low Risk (<40%)': len([c for c in customers if c['churn_probability'] < 0.4])
    }
    
    # チャーンリスク可視化
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚨 チャーンリスク分布")
        
        risk_colors = ['#ef4444', '#f59e0b', '#10b981']
        
        fig_churn = px.pie(
            values=list(churn_levels.values()),
            names=list(churn_levels.keys()),
            color_discrete_sequence=risk_colors
        )
        
        fig_churn.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_churn, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 チャーン要因分析")
        
        churn_factors = {
            '低エンゲージメント': 0.45,
            '長期未購入': 0.32,
            '競合流出': 0.28,
            'サポート問題': 0.18,
            '価格不満': 0.15,
            '機能不足': 0.12
        }
        
        fig_factors = px.bar(
            x=list(churn_factors.values()),
            y=list(churn_factors.keys()),
            orientation='h',
            color=list(churn_factors.values()),
            color_continuous_scale="Reds"
        )
        
        fig_factors.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_title="影響度"
        )
        
        st.plotly_chart(fig_factors, use_container_width=True)
    
    # 高リスク顧客リスト
    st.markdown("#### 🚨 緊急対応必要顧客")
    
    high_risk_customers = [c for c in customers if c['churn_probability'] >= 0.7]
    high_risk_customers.sort(key=lambda x: x['churn_probability'], reverse=True)
    
    for customer in high_risk_customers[:10]:
        churn_class = "churn-high" if customer['churn_probability'] >= 0.8 else "churn-prediction"
        
        st.markdown(f"""
        <div class="{churn_class}">
            <div style="display: flex; justify-content: between; align-items: center;">
                <div>
                    <h4 style="color: #ef4444; margin-bottom: 10px;">{customer['id']}</h4>
                    <div>
                        <strong>ステージ:</strong> {customer['stage']}<br>
                        <strong>LTV:</strong> ¥{customer['ltv']:,.0f}<br>
                        <strong>最終購入:</strong> {customer['last_purchase'].strftime('%Y-%m-%d')}<br>
                        <strong>エンゲージメント:</strong> {customer['engagement_score']*100:.0f}%
                    </div>
                </div>
                <div class="churn-score">
                    <div class="churn-percentage">{customer['churn_probability']*100:.0f}%</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">チャーン確率</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 推奨アクション
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"📧 緊急メール送信", key=f"email_{customer['id']}"):
                st.success(f"✅ {customer['id']}に緊急挽留メールを送信しました")
        
        with col2:
            if st.button(f"☎️ 個別コンタクト", key=f"call_{customer['id']}"):
                st.success(f"📞 {customer['id']}への個別コンタクトを予約しました")
        
        with col3:
            if st.button(f"🎁 特別オファー", key=f"offer_{customer['id']}"):
                st.success(f"🎯 {customer['id']}に特別オファーを配信しました")
        
        st.markdown("---")
    
    # チャーン防止キャンペーン効果
    st.markdown("#### 📈 チャーン防止キャンペーン効果")
    
    campaign_results = {
        'パーソナライズメール': {'success_rate': 0.35, 'cost_per_retention': 2500},
        '限定オファー': {'success_rate': 0.42, 'cost_per_retention': 4200},
        '個別コンサルテーション': {'success_rate': 0.58, 'cost_per_retention': 8500},
        'VIP待遇アップグレード': {'success_rate': 0.48, 'cost_per_retention': 5800}
    }
    
    for campaign, results in campaign_results.items():
        roi = (20000 * results['success_rate'] - results['cost_per_retention']) / results['cost_per_retention'] * 100
        roi_class = "roi-positive" if roi > 0 else "roi-negative"
        
        st.markdown(f"""
        <div class="optimization-card">
            <div class="optimization-header">
                <div class="optimization-title">{campaign}</div>
                <div class="optimization-impact">ROI: {roi:+.0f}%</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 10px;">
                <div style="text-align: center;">
                    <div style="color: #06b6d4; font-weight: bold;">{results['success_rate']*100:.0f}%</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">成功率</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #ef4444; font-weight: bold;">¥{results['cost_per_retention']:,}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">顧客当たりコスト</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #10b981; font-weight: bold;">¥{results['success_rate'] * 20000:,.0f}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">期待挽留価値</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 最適化提案タブ
with tabs[4]:
    st.markdown("### 📊 AI最適化提案")
    
    # 全体最適化サマリー
    st.markdown("#### 🎯 全体最適化サマリー")
    
    optimization_opportunities = [
        {
            'area': 'Awareness → Consideration転換',
            'current': '62%',
            'potential': '78%',
            'impact': '+¥2.4M 年間収益',
            'effort': 'Medium',
            'recommendation': 'コンテンツマーケティング強化、SEO最適化'
        },
        {
            'area': 'Trial → Purchase転換',
            'current': '28%',
            'potential': '45%',
            'impact': '+¥3.8M 年間収益',
            'effort': 'High',
            'recommendation': 'オンボーディング改善、トライアル期間最適化'
        },
        {
            'area': 'チャーン率削減',
            'current': '18%',
            'potential': '12%',
            'impact': '+¥1.9M 挽留価値',
            'effort': 'Medium',
            'recommendation': 'エンゲージメント向上、プロアクティブサポート'
        },
        {
            'area': 'LTV向上',
            'current': '¥22k',
            'potential': '¥31k',
            'impact': '+¥9M 総価値向上',
            'effort': 'Low',
            'recommendation': 'アップセル・クロスセル自動化'
        }
    ]
    
    for opt in optimization_opportunities:
        effort_colors = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
        effort_color = effort_colors.get(opt['effort'], '#06b6d4')
        
        st.markdown(f"""
        <div class="prediction-insight">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div class="insight-title">{opt['area']}</div>
                <div style="background: {effort_color}; color: white; padding: 4px 12px; border-radius: 15px; font-size: 0.8rem;">
                    {opt['effort']} 難易度
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 15px;">
                <div style="text-align: center;">
                    <div style="color: #ef4444; font-weight: bold; font-size: 1.2rem;">{opt['current']}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">現在</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #10b981; font-weight: bold; font-size: 1.2rem;">{opt['potential']}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">目標</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #06b6d4; font-weight: bold; font-size: 1.2rem;">{opt['impact']}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">インパクト</div>
                </div>
            </div>
            <div style="background: rgba(6, 182, 212, 0.1); padding: 10px; border-radius: 8px;">
                <strong>推奨アクション:</strong> {opt['recommendation']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 優先度マトリックス
    st.markdown("#### 📈 優先度マトリックス")
    
    # インパクト vs 実装難易度
    impact_values = [2.4, 3.8, 1.9, 9.0]  # Million円
    effort_values = [2, 3, 2, 1]  # 1=Low, 2=Medium, 3=High
    area_names = [opt['area'] for opt in optimization_opportunities]
    
    fig_matrix = px.scatter(
        x=effort_values,
        y=impact_values,
        size=[abs(val) for val in impact_values],
        color=impact_values,
        hover_name=area_names,
        labels={'x': '実装難易度', 'y': 'インパクト (百万円)'},
        title="最適化優先度マトリックス",
        color_continuous_scale="Viridis"
    )
    
    fig_matrix.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(tickmode='array', tickvals=[1, 2, 3], ticktext=['Low', 'Medium', 'High'])
    )
    
    # 理想的な領域をハイライト
    fig_matrix.add_shape(
        type="rect",
        x0=0.5, y0=3, x1=2.5, y1=10,
        fillcolor="rgba(16, 185, 129, 0.1)",
        line=dict(color="rgba(16, 185, 129, 0.3)", width=2),
    )
    
    fig_matrix.add_annotation(
        x=1.5, y=6.5,
        text="Quick Wins",
        showarrow=False,
        font=dict(color="#10b981", size=14, family="Arial Black")
    )
    
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    # 実装ロードマップ
    st.markdown("#### 🗓️ 実装ロードマップ")
    
    roadmap_items = [
        {'month': 'Month 1', 'item': 'アップセル・クロスセル自動化', 'status': 'ready'},
        {'month': 'Month 2', 'item': 'コンテンツマーケティング強化', 'status': 'planning'},
        {'month': 'Month 3', 'item': 'エンゲージメント向上施策', 'status': 'planning'},
        {'month': 'Month 4-6', 'item': 'オンボーディング改善プロジェクト', 'status': 'future'}
    ]
    
    for item in roadmap_items:
        status_colors = {'ready': '#10b981', 'planning': '#f59e0b', 'future': '#94a3b8'}
        status_color = status_colors.get(item['status'], '#06b6d4')
        
        st.markdown(f"""
        <div class="lifecycle-stage" style="border-left-color: {status_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h5 style="color: {status_color}; margin-bottom: 5px;">{item['month']}</h5>
                    <div style="color: #e2e8f0;">{item['item']}</div>
                </div>
                <div style="background: {status_color}; color: white; padding: 4px 12px; border-radius: 15px; font-size: 0.8rem;">
                    {item['status'].upper()}
                </div>
            </div>
            <div class="lifecycle-progress">
                <div class="lifecycle-fill" style="width: {'100' if item['status'] == 'ready' else '60' if item['status'] == 'planning' else '0'}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("🛤️ ジャーニーエンジン")
    
    # リアルタイム監視
    st.subheader("📡 リアルタイム監視")
    
    st.markdown("""
    <div class="realtime-data">
        <div class="realtime-indicator"></div>
        <h5 style="color: #06b6d4; margin-bottom: 10px;">ライブアクティビティ</h5>
        <div style="font-size: 0.9rem; color: #94a3b8;">
            • 3分前: 新規顧客がTrial開始<br>
            • 7分前: High-Valueセグメント購入<br>
            • 12分前: At-Risk顧客エンゲージ<br>
            • 18分前: ジャーニーステージ遷移
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 今日の統計
    st.subheader("📊 本日の統計")
    
    st.metric("新規顧客", "47", "+12")
    st.metric("ステージ遷移", "123", "+8")
    st.metric("チャーン防止", "15", "+3")
    
    conversion_today = np.random.uniform(15, 25)
    st.metric("総合転換率", f"{conversion_today:.1f}%", "+2.3%")
    
    st.markdown("---")
    
    # AI予測精度
    st.subheader("🤖 AI予測精度")
    
    accuracy_metrics = [
        ("購入予測", 94.2),
        ("チャーン予測", 87.8),
        ("LTV予測", 91.5),
        ("セグメント分類", 96.1)
    ]
    
    for metric, accuracy in accuracy_metrics:
        st.markdown(f"**{metric}**: {accuracy}%")
        st.progress(accuracy / 100)
    
    st.markdown("---")
    
    # 緊急アラート
    st.subheader("🚨 緊急アラート")
    
    urgent_alerts = [
        {"level": "high", "message": "高価値顧客のチャーンリスク急上昇", "time": "5分前"},
        {"level": "medium", "message": "Trial→Purchase転換率低下", "time": "1時間前"},
        {"level": "low", "message": "新セグメント形成を検出", "time": "3時間前"}
    ]
    
    for alert in urgent_alerts:
        alert_icons = {"high": "🔴", "medium": "🟡", "low": "🔵"}
        st.markdown(f"{alert_icons[alert['level']]} {alert['message']}")
        st.caption(alert['time'])
    
    st.markdown("---")
    
    # 自動化設定
    st.subheader("⚙️ 自動化設定")
    
    auto_churn_prevention = st.checkbox("チャーン防止自動実行", value=True)
    auto_segmentation = st.checkbox("リアルタイムセグメント更新", value=True)
    auto_recommendations = st.checkbox("AI推奨アクション", value=True)
    
    st.markdown("---")
    
    # エクスポート・レポート
    st.subheader("📥 エクスポート")
    
    if st.button("📊 ジャーニー分析レポート", use_container_width=True):
        st.success("📈 詳細ジャーニー分析レポートを生成中...")
    
    if st.button("💾 顧客データエクスポート", use_container_width=True):
        export_data = {
            "customers": len(customers),
            "segments": len(customer_segments),
            "journey_stages": list(journey_metrics.keys()),
            "export_timestamp": datetime.now().isoformat()
        }
        
        st.download_button(
            "📥 JSONダウンロード",
            data=json.dumps(export_data, ensure_ascii=False, indent=2),
            file_name=f"customer_journey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("🎯 アトリビューション分析", use_container_width=True):
        st.switch_page("pages/attribution_analysis.py")
    
    if st.button("⚡ リアルタイム最適化", use_container_width=True):
        st.switch_page("pages/realtime_ad_optimizer.py")

# フッター
st.markdown("---")
st.caption("🛤️ Customer Journey Engine: AI駆動の次世代顧客ジャーニー分析で、すべての顧客体験を最適化し、ビジネス成長を加速させます。")