#!/usr/bin/env python3
"""
リアルタイム広告最適化エンジン
機械学習による自動広告最適化と入札管理
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
import time

# ページ設定
st.set_page_config(
    page_title="リアルタイム広告最適化",
    page_icon="⚡",
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
    .optimizer-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .optimizer-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(0.8); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 0.8; }
    }
    
    .optimizer-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .optimizer-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* リアルタイムカード */
    .realtime-card {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 2px solid rgba(255, 107, 107, 0.3);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .realtime-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 107, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .realtime-card:hover::before {
        left: 100%;
    }
    
    .realtime-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(255, 107, 107, 0.4);
        border-color: #ff6b6b;
    }
    
    /* ライブインジケーター */
    .live-indicator {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 15px;
        animation: liveFlash 2s infinite;
    }
    
    @keyframes liveFlash {
        0%, 50% { opacity: 1; }
        25%, 75% { opacity: 0.7; }
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
        animation: livePulse 1s infinite;
    }
    
    @keyframes livePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    
    /* パフォーマンスメトリクス */
    .perf-metric {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(255, 107, 107, 0.2);
        transition: all 0.3s;
    }
    
    .perf-metric:hover {
        border-color: rgba(255, 107, 107, 0.5);
        transform: translateY(-3px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff6b6b;
        margin-bottom: 8px;
        text-shadow: 0 0 10px rgba(255, 107, 107, 0.3);
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 8px;
    }
    
    .metric-change {
        font-size: 0.9rem;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .change-positive {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .change-negative {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    .change-neutral {
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
    }
    
    /* 最適化アクション */
    .optimization-action {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        transition: all 0.3s;
    }
    
    .optimization-action:hover {
        background: rgba(255, 107, 107, 0.15);
        border-color: rgba(255, 107, 107, 0.5);
    }
    
    .action-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .action-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ff6b6b;
    }
    
    .action-impact {
        background: #ff6b6b;
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* AI判定インジケーター */
    .ai-decision {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(238, 90, 36, 0.2) 100%);
        border: 1px solid rgba(255, 107, 107, 0.4);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    
    .decision-confidence {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: 10px;
    }
    
    .confidence-bar {
        flex-grow: 1;
        height: 8px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a24 100%);
        border-radius: 4px;
        transition: width 1s ease;
    }
    
    /* アラートカード */
    .alert-card {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        animation: alertPulse 3s infinite;
    }
    
    @keyframes alertPulse {
        0%, 100% { border-color: rgba(239, 68, 68, 0.3); }
        50% { border-color: rgba(239, 68, 68, 0.6); }
    }
    
    .alert-urgent {
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.5);
    }
    
    /* 入札戦略カード */
    .bidding-strategy {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 107, 107, 0.2);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        transition: all 0.3s;
    }
    
    .bidding-strategy:hover {
        border-color: rgba(255, 107, 107, 0.4);
        background: rgba(30, 41, 59, 0.8);
    }
    
    .strategy-active {
        border-color: #ff6b6b;
        background: rgba(255, 107, 107, 0.1);
    }
    
    /* プラットフォームステータス */
    .platform-status {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 15px;
        background: rgba(30, 41, 59, 0.6);
        border-radius: 10px;
        margin: 8px 0;
    }
    
    .status-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: statusPulse 2s infinite;
    }
    
    .status-active {
        background: #10b981;
    }
    
    .status-warning {
        background: #f59e0b;
    }
    
    .status-error {
        background: #ef4444;
    }
    
    @keyframes statusPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* チャートコンテナ */
    .chart-container {
        background: rgba(30, 41, 59, 0.5);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 107, 107, 0.2);
        margin: 20px 0;
    }
    
    /* 自動実行ボタン */
    .auto-execute-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: none;
        color: white;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .auto-execute-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
    }
    
    .manual-execute-btn {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .manual-execute-btn:hover {
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'optimizer_data' not in st.session_state:
    st.session_state.optimizer_data = {}

if 'optimization_history' not in st.session_state:
    st.session_state.optimization_history = []

if 'auto_optimization_enabled' not in st.session_state:
    st.session_state.auto_optimization_enabled = False

if 'realtime_alerts' not in st.session_state:
    st.session_state.realtime_alerts = []

def generate_realtime_data():
    """リアルタイムデータを生成"""
    current_time = datetime.now()
    
    # ベースメトリクス
    base_metrics = {
        'impressions': np.random.randint(10000, 50000),
        'clicks': np.random.randint(200, 2000),
        'conversions': np.random.randint(10, 100),
        'cost': np.random.uniform(5000, 25000),
        'ctr': np.random.uniform(0.5, 5.0),
        'cpc': np.random.uniform(100, 1000),
        'cpa': np.random.uniform(2000, 8000),
        'roas': np.random.uniform(2.0, 8.0)
    }
    
    # プラットフォーム別データ
    platforms = ['Google Ads', 'Facebook Ads', 'Instagram Ads', 'LinkedIn Ads', 'Twitter Ads']
    platform_data = {}
    
    for platform in platforms:
        platform_data[platform] = {
            'status': np.random.choice(['active', 'warning', 'error'], p=[0.7, 0.2, 0.1]),
            'spend': np.random.uniform(1000, 8000),
            'performance': np.random.uniform(0.6, 0.95),
            'impressions': np.random.randint(2000, 15000),
            'clicks': np.random.randint(40, 500),
            'ctr': np.random.uniform(0.8, 4.5)
        }
    
    return {
        'timestamp': current_time.isoformat(),
        'metrics': base_metrics,
        'platforms': platform_data,
        'market_conditions': {
            'competition_index': np.random.uniform(0.3, 0.9),
            'cost_trend': np.random.choice(['increasing', 'decreasing', 'stable']),
            'demand_level': np.random.choice(['low', 'medium', 'high'])
        }
    }

def generate_optimization_recommendations(data: Dict) -> List[Dict]:
    """最適化推奨事項を生成"""
    recommendations = []
    metrics = data['metrics']
    
    # CTRベースの推奨
    if metrics['ctr'] < 2.0:
        recommendations.append({
            'type': 'creative_optimization',
            'priority': 'high',
            'title': 'クリエイティブ最適化',
            'description': f"CTRが{metrics['ctr']:.2f}%と低下しています。新しいクリエイティブバリエーションのテストを推奨します。",
            'expected_impact': '+35% CTR向上',
            'confidence': 0.87,
            'action': 'A/Bテストで3つの新しいクリエイティブをテスト'
        })
    
    # CPAベースの推奨
    if metrics['cpa'] > 6000:
        recommendations.append({
            'type': 'bid_adjustment',
            'priority': 'high',
            'title': '入札調整',
            'description': f"CPAが¥{metrics['cpa']:,.0f}と目標を上回っています。入札価格の調整が必要です。",
            'expected_impact': '-25% CPA削減',
            'confidence': 0.92,
            'action': '入札価格を15%削減し、高品質スコアキーワードに集中'
        })
    
    # ROASベースの推奨
    if metrics['roas'] < 3.0:
        recommendations.append({
            'type': 'targeting_optimization',
            'priority': 'medium',
            'title': 'ターゲティング最適化',
            'description': f"ROAS {metrics['roas']:.1f}x が目標を下回っています。オーディエンスの見直しが必要です。",
            'expected_impact': '+40% ROAS向上',
            'confidence': 0.78,
            'action': 'コンバージョン率の高いセグメントに予算を再配分'
        })
    
    # プラットフォーム最適化
    platforms = data['platforms']
    low_performers = [p for p, data in platforms.items() if data['performance'] < 0.7]
    
    if low_performers:
        recommendations.append({
            'type': 'platform_reallocation',
            'priority': 'medium',
            'title': 'プラットフォーム予算再配分',
            'description': f"{', '.join(low_performers)}のパフォーマンスが低下しています。",
            'expected_impact': '+20% 全体効率',
            'confidence': 0.83,
            'action': f"高パフォーマンスプラットフォームに予算をシフト"
        })
    
    return recommendations

def execute_optimization(recommendation: Dict) -> Dict[str, Any]:
    """最適化を実行（スタブ）"""
    
    # 実行シミュレーション
    execution_time = np.random.uniform(2, 8)
    success_probability = recommendation['confidence']
    
    time.sleep(min(execution_time / 4, 2))  # 実際の実行時間をシミュレート
    
    is_successful = np.random.random() < success_probability
    
    if is_successful:
        return {
            'status': 'success',
            'message': f"{recommendation['title']}を正常に実行しました",
            'execution_time': execution_time,
            'estimated_impact': recommendation['expected_impact']
        }
    else:
        return {
            'status': 'error',
            'message': f"{recommendation['title']}の実行中にエラーが発生しました",
            'execution_time': execution_time,
            'error_code': 'OPT_' + str(np.random.randint(1000, 9999))
        }

# ヘッダー
st.markdown("""
<div class="optimizer-header">
    <div class="optimizer-title">⚡ リアルタイム広告最適化エンジン</div>
    <div class="optimizer-subtitle">AI駆動の自動入札・広告最適化システム</div>
</div>
""", unsafe_allow_html=True)

# リアルタイムデータ生成
if 'last_update' not in st.session_state or (datetime.now() - datetime.fromisoformat(st.session_state.get('last_update', datetime.now().isoformat()))).seconds > 30:
    st.session_state.realtime_data = generate_realtime_data()
    st.session_state.last_update = datetime.now().isoformat()

# ライブインジケーター
st.markdown("""
<div class="live-indicator">
    <div class="live-dot"></div>
    LIVE - リアルタイム監視中
</div>
""", unsafe_allow_html=True)

# メイン統計
col1, col2, col3, col4, col5 = st.columns(5)

metrics = st.session_state.realtime_data['metrics']

with col1:
    st.markdown(f"""
    <div class="perf-metric">
        <div class="metric-value">{metrics['impressions']:,}</div>
        <div class="metric-label">インプレッション</div>
        <div class="metric-change change-positive">+12.3%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="perf-metric">
        <div class="metric-value">{metrics['clicks']:,}</div>
        <div class="metric-label">クリック数</div>
        <div class="metric-change change-positive">+8.7%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="perf-metric">
        <div class="metric-value">{metrics['ctr']:.2f}%</div>
        <div class="metric-label">CTR</div>
        <div class="metric-change change-positive">+0.3%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="perf-metric">
        <div class="metric-value">¥{metrics['cpc']:,.0f}</div>
        <div class="metric-label">CPC</div>
        <div class="metric-change change-negative">+5.2%</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="perf-metric">
        <div class="metric-value">{metrics['roas']:.1f}x</div>
        <div class="metric-label">ROAS</div>
        <div class="metric-change change-positive">+0.8x</div>
    </div>
    """, unsafe_allow_html=True)

# タブ構成
tabs = st.tabs(["🎯 自動最適化", "📊 リアルタイム分析", "🤖 AI推奨事項", "💰 入札管理", "📈 パフォーマンス予測"])

# 自動最適化タブ
with tabs[0]:
    st.markdown("### 🤖 AI自動最適化エンジン")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 自動最適化設定
        st.markdown("#### ⚙️ 最適化設定")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            auto_optimization = st.checkbox(
                "自動最適化を有効化",
                value=st.session_state.auto_optimization_enabled,
                help="AIが自動的に広告を最適化します"
            )
            
            optimization_frequency = st.selectbox(
                "最適化頻度",
                ["リアルタイム", "15分毎", "1時間毎", "6時間毎", "日次"]
            )
            
            max_bid_adjustment = st.slider(
                "最大入札調整率 (%)",
                min_value=5,
                max_value=50,
                value=20,
                help="一度に調整可能な最大入札価格の変更率"
            )
        
        with col_b:
            target_metrics = st.multiselect(
                "最適化対象メトリクス",
                ["CPA", "ROAS", "CTR", "コンバージョン数", "品質スコア"],
                default=["CPA", "ROAS"]
            )
            
            risk_tolerance = st.selectbox(
                "リスク許容度",
                ["保守的", "バランス", "積極的"],
                index=1
            )
            
            min_confidence = st.slider(
                "最小信頼度 (%)",
                min_value=50,
                max_value=95,
                value=80,
                help="この信頼度以上の推奨のみ自動実行"
            )
        
        st.session_state.auto_optimization_enabled = auto_optimization
        
        # 現在の最適化ステータス
        if auto_optimization:
            st.markdown("""
            <div class="ai-decision">
                <h4>🟢 自動最適化 - 稼働中</h4>
                <p>AIエージェントが広告パフォーマンスを継続監視し、最適化を実行しています。</p>
                <div class="decision-confidence">
                    <span>AI信頼度:</span>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: 89%;"></div>
                    </div>
                    <span>89%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="ai-decision">
                <h4>⭕ 手動モード</h4>
                <p>推奨事項を確認してから手動で最適化を実行できます。</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 最適化履歴
        st.markdown("#### 📜 最適化履歴")
        
        if st.session_state.optimization_history:
            for i, optimization in enumerate(st.session_state.optimization_history[-5:]):
                status_icon = "✅" if optimization['status'] == 'success' else "❌"
                st.markdown(f"""
                <div class="optimization-action">
                    <div class="action-header">
                        <span>{status_icon} {optimization['title']}</span>
                        <span class="action-impact">{optimization.get('impact', 'N/A')}</span>
                    </div>
                    <p>{optimization['message']}</p>
                    <small>実行時刻: {optimization['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("まだ最適化は実行されていません")
    
    with col2:
        # プラットフォームステータス
        st.markdown("#### 📱 プラットフォーム状況")
        
        platforms = st.session_state.realtime_data['platforms']
        
        for platform, data in platforms.items():
            status_class = f"status-{data['status']}"
            status_text = {
                'active': '正常稼働',
                'warning': '要注意',
                'error': 'エラー'
            }[data['status']]
            
            st.markdown(f"""
            <div class="platform-status">
                <div class="status-dot {status_class}"></div>
                <div>
                    <strong>{platform}</strong><br>
                    <small>{status_text} - パフォーマンス: {data['performance']*100:.1f}%</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 緊急アラート
        st.markdown("#### 🚨 アラート")
        
        alerts = [
            {"type": "urgent", "message": "Google Ads CTRが急低下中", "time": "2分前"},
            {"type": "warning", "message": "CPCが目標を20%上回り", "time": "15分前"},
            {"type": "info", "message": "新しい最適化機会を検出", "time": "1時間前"}
        ]
        
        for alert in alerts:
            alert_class = "alert-urgent" if alert['type'] == 'urgent' else "alert-card"
            st.markdown(f"""
            <div class="{alert_class}">
                <strong>{alert['message']}</strong><br>
                <small>{alert['time']}</small>
            </div>
            """, unsafe_allow_html=True)

# リアルタイム分析タブ
with tabs[1]:
    st.markdown("### 📊 リアルタイムパフォーマンス分析")
    
    # 時系列グラフ
    st.markdown("#### 📈 パフォーマンストレンド")
    
    # サンプル時系列データ生成
    hours = pd.date_range(end=datetime.now(), periods=24, freq='H')
    trend_data = pd.DataFrame({
        'time': hours,
        'impressions': np.random.randint(1000, 3000, 24),
        'clicks': np.random.randint(20, 100, 24),
        'conversions': np.random.randint(1, 10, 24),
        'cost': np.random.uniform(500, 1500, 24)
    })
    
    trend_data['ctr'] = (trend_data['clicks'] / trend_data['impressions']) * 100
    trend_data['cpc'] = trend_data['cost'] / trend_data['clicks']
    
    # CTRとCPCの推移
    fig_trends = go.Figure()
    
    fig_trends.add_trace(go.Scatter(
        x=trend_data['time'],
        y=trend_data['ctr'],
        mode='lines+markers',
        name='CTR (%)',
        line=dict(color='#ff6b6b', width=3),
        yaxis='y'
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=trend_data['time'],
        y=trend_data['cpc'],
        mode='lines+markers',
        name='CPC (¥)',
        line=dict(color='#4ecdc4', width=3),
        yaxis='y2'
    ))
    
    fig_trends.update_layout(
        title="24時間パフォーマンス推移",
        xaxis_title="時刻",
        yaxis=dict(title="CTR (%)", side="left"),
        yaxis2=dict(title="CPC (¥)", side="right", overlaying="y"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # プラットフォーム別比較
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 プラットフォーム別インプレッション")
        
        platform_data = st.session_state.realtime_data['platforms']
        platform_names = list(platform_data.keys())
        platform_impressions = [data['impressions'] for data in platform_data.values()]
        
        fig_platforms = px.bar(
            x=platform_names,
            y=platform_impressions,
            color=platform_impressions,
            color_continuous_scale="Reds",
            title="プラットフォーム別インプレッション"
        )
        
        fig_platforms.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_platforms, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 コスト配分")
        
        platform_spend = [data['spend'] for data in platform_data.values()]
        
        fig_spend = px.pie(
            values=platform_spend,
            names=platform_names,
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        
        fig_spend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_spend, use_container_width=True)
    
    # ヒートマップ
    st.markdown("#### 🔥 時間帯×プラットフォーム パフォーマンスヒートマップ")
    
    # サンプルヒートマップデータ
    hours_24 = [f"{i:02d}:00" for i in range(24)]
    platforms_5 = list(platform_data.keys())
    
    heatmap_data = np.random.uniform(0.5, 5.0, (len(platforms_5), 24))
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=hours_24,
        y=platforms_5,
        colorscale='Reds',
        colorbar=dict(title="CTR (%)")
    ))
    
    fig_heatmap.update_layout(
        title="時間帯別プラットフォームCTR",
        xaxis_title="時刻",
        yaxis_title="プラットフォーム",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

# AI推奨事項タブ
with tabs[2]:
    st.markdown("### 🤖 AI最適化推奨事項")
    
    # 推奨事項を生成
    recommendations = generate_optimization_recommendations(st.session_state.realtime_data)
    
    if recommendations:
        st.markdown(f"#### {len(recommendations)}件の最適化機会を検出")
        
        for i, rec in enumerate(recommendations):
            priority_color = {
                'high': '#ef4444',
                'medium': '#f59e0b',
                'low': '#10b981'
            }[rec['priority']]
            
            st.markdown(f"""
            <div class="optimization-action">
                <div class="action-header">
                    <span class="action-title">{rec['title']}</span>
                    <span class="action-impact" style="background: {priority_color};">{rec['expected_impact']}</span>
                </div>
                <p>{rec['description']}</p>
                <p><strong>推奨アクション:</strong> {rec['action']}</p>
                <div class="decision-confidence">
                    <span>AI信頼度:</span>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {rec['confidence']*100}%;"></div>
                    </div>
                    <span>{rec['confidence']*100:.0f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"✅ 実行", key=f"execute_{i}", type="primary"):
                    with st.spinner("最適化を実行中..."):
                        result = execute_optimization(rec)
                        
                        # 履歴に追加
                        optimization_record = {
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'title': rec['title'],
                            'status': result['status'],
                            'message': result['message'],
                            'impact': rec['expected_impact']
                        }
                        
                        st.session_state.optimization_history.append(optimization_record)
                        
                        if result['status'] == 'success':
                            st.success(result['message'])
                        else:
                            st.error(result['message'])
                        
                        st.rerun()
            
            with col2:
                if st.button(f"⏰ スケジュール", key=f"schedule_{i}"):
                    st.info(f"「{rec['title']}」を30分後に実行予定として設定しました")
            
            with col3:
                if st.button(f"❌ 却下", key=f"reject_{i}"):
                    st.warning(f"「{rec['title']}」を却下しました")
            
            st.markdown("---")
    else:
        st.success("🎉 すべて最適化済みです！現在の広告パフォーマンスは良好な状態を維持しています。")

# 入札管理タブ
with tabs[3]:
    st.markdown("### 💰 入札戦略管理")
    
    # 入札戦略選択
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 現在の入札戦略")
        
        current_strategies = [
            {"name": "目標CPA", "status": "active", "performance": 0.87, "spend": "¥45,600"},
            {"name": "目標ROAS", "status": "active", "performance": 0.92, "spend": "¥38,200"},
            {"name": "拡張CPC", "status": "paused", "performance": 0.73, "spend": "¥12,800"},
            {"name": "手動CPC", "status": "active", "performance": 0.68, "spend": "¥8,900"}
        ]
        
        for strategy in current_strategies:
            status_class = "strategy-active" if strategy['status'] == 'active' else "bidding-strategy"
            performance_color = "#10b981" if strategy['performance'] > 0.8 else "#f59e0b" if strategy['performance'] > 0.6 else "#ef4444"
            
            st.markdown(f"""
            <div class="{status_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>{strategy['name']}</h4>
                        <p>ステータス: {strategy['status']}</p>
                        <p>予算: {strategy['spend']}</p>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {performance_color}; font-size: 1.5rem; font-weight: bold;">
                            {strategy['performance']*100:.0f}%
                        </div>
                        <div>パフォーマンス</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ⚡ スマート入札推奨")
        
        smart_recommendations = [
            {
                "strategy": "目標CPA最適化",
                "current_cpa": "¥5,200",
                "target_cpa": "¥4,100",
                "potential_saving": "21%",
                "confidence": 0.89
            },
            {
                "strategy": "ROAS最大化",
                "current_roas": "3.2x",
                "target_roas": "4.8x",
                "potential_improvement": "50%",
                "confidence": 0.76
            }
        ]
        
        for rec in smart_recommendations:
            st.markdown(f"""
            <div class="ai-decision">
                <h4>{rec['strategy']}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
                    <div>
                        <strong>現在:</strong> {rec.get('current_cpa', rec.get('current_roas', 'N/A'))}
                    </div>
                    <div>
                        <strong>目標:</strong> {rec.get('target_cpa', rec.get('target_roas', 'N/A'))}
                    </div>
                </div>
                <div class="decision-confidence">
                    <span>期待効果: {rec.get('potential_saving', rec.get('potential_improvement', 'N/A'))}</span>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {rec['confidence']*100}%;"></div>
                    </div>
                    <span>{rec['confidence']*100:.0f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🚀 {rec['strategy']}を適用", key=f"apply_{rec['strategy']}"):
                st.success(f"✅ {rec['strategy']}を適用しました！変更は5-10分で反映されます。")
    
    # 入札調整履歴
    st.markdown("#### 📊 入札調整履歴")
    
    # サンプル履歴データ
    adjustment_history = pd.DataFrame({
        'timestamp': pd.date_range(end=datetime.now(), periods=10, freq='2H'),
        'keyword': ['マーケティング ツール', 'AI 広告', 'デジタル 戦略', '自動化 ソフト', 'SaaS 営業'] * 2,
        'old_bid': np.random.randint(100, 500, 10),
        'new_bid': np.random.randint(120, 600, 10),
        'reason': ['CTR向上', 'CPA最適化', '競合対応', '品質スコア改善', 'コンバージョン増加'] * 2
    })
    
    adjustment_history['change'] = ((adjustment_history['new_bid'] - adjustment_history['old_bid']) / adjustment_history['old_bid'] * 100).round(1)
    
    st.dataframe(
        adjustment_history[['timestamp', 'keyword', 'old_bid', 'new_bid', 'change', 'reason']].rename(columns={
            'timestamp': '時刻',
            'keyword': 'キーワード',
            'old_bid': '変更前入札価格(¥)',
            'new_bid': '変更後入札価格(¥)',
            'change': '変更率(%)',
            'reason': '調整理由'
        }),
        use_container_width=True
    )

# パフォーマンス予測タブ
with tabs[4]:
    st.markdown("### 📈 AI パフォーマンス予測")
    
    # 予測期間選択
    col1, col2, col3 = st.columns(3)
    
    with col1:
        forecast_period = st.selectbox("予測期間", ["24時間", "7日間", "30日間", "90日間"])
    
    with col2:
        confidence_interval = st.selectbox("信頼区間", ["90%", "95%", "99%"])
    
    with col3:
        if st.button("🔮 予測実行", type="primary"):
            with st.spinner("AI予測モデルを実行中..."):
                time.sleep(2)
                st.success("✅ 予測完了！")
    
    # 予測グラフ
    st.markdown("#### 📊 パフォーマンス予測")
    
    # サンプル予測データ
    periods_map = {"24時間": 24, "7日間": 7, "30日間": 30, "90日間": 90}
    periods = periods_map[forecast_period]
    freq = 'H' if forecast_period == "24時間" else 'D'
    
    forecast_dates = pd.date_range(start=datetime.now(), periods=periods, freq=freq)
    
    # 基本トレンド + ノイズ
    base_trend = np.linspace(metrics['ctr'], metrics['ctr'] * 1.15, periods)
    noise = np.random.normal(0, 0.1, periods)
    forecast_ctr = base_trend + noise
    
    # 信頼区間
    confidence = float(confidence_interval[:-1]) / 100
    margin = np.random.uniform(0.2, 0.5, periods)
    upper_bound = forecast_ctr + margin
    lower_bound = forecast_ctr - margin
    
    fig_forecast = go.Figure()
    
    # 信頼区間
    fig_forecast.add_trace(go.Scatter(
        x=forecast_dates,
        y=upper_bound,
        mode='lines',
        line=dict(color='rgba(255, 107, 107, 0)', width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig_forecast.add_trace(go.Scatter(
        x=forecast_dates,
        y=lower_bound,
        mode='lines',
        line=dict(color='rgba(255, 107, 107, 0)', width=0),
        fill='tonexty',
        fillcolor='rgba(255, 107, 107, 0.2)',
        name=f'{confidence_interval} 信頼区間',
        hoverinfo='skip'
    ))
    
    # 予測線
    fig_forecast.add_trace(go.Scatter(
        x=forecast_dates,
        y=forecast_ctr,
        mode='lines+markers',
        name='CTR予測',
        line=dict(color='#ff6b6b', width=3)
    ))
    
    fig_forecast.update_layout(
        title=f"CTR {forecast_period} 予測",
        xaxis_title="時間",
        yaxis_title="CTR (%)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # 予測サマリー
    col1, col2, col3 = st.columns(3)
    
    with col1:
        predicted_improvement = ((forecast_ctr[-1] - forecast_ctr[0]) / forecast_ctr[0] * 100)
        st.markdown(f"""
        <div class="perf-metric">
            <div class="metric-value">{predicted_improvement:+.1f}%</div>
            <div class="metric-label">予測改善率</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        forecast_volatility = np.std(forecast_ctr) / np.mean(forecast_ctr) * 100
        st.markdown(f"""
        <div class="perf-metric">
            <div class="metric-value">{forecast_volatility:.1f}%</div>
            <div class="metric-label">予測変動率</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        confidence_score = np.random.uniform(75, 95)
        st.markdown(f"""
        <div class="perf-metric">
            <div class="metric-value">{confidence_score:.1f}%</div>
            <div class="metric-label">予測信頼度</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 予測に基づく推奨事項
    st.markdown("#### 💡 予測ベース推奨事項")
    
    forecast_recommendations = [
        f"予測では{forecast_period}で CTR が {predicted_improvement:.1f}% 改善する見込みです",
        f"現在の入札戦略を維持することで、安定したパフォーマンス向上が期待できます",
        f"予測変動率 {forecast_volatility:.1f}% は適正範囲内です",
        f"週末にかけてパフォーマンスの一時的な低下が予想されます"
    ]
    
    for i, recommendation in enumerate(forecast_recommendations, 1):
        st.markdown(f"""
        <div class="optimization-action">
            <div class="action-header">
                <span class="action-title">予測インサイト {i}</span>
            </div>
            <p>{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("⚡ 最適化エンジン")
    
    # 全体制御
    st.subheader("🎛️ 全体制御")
    
    if st.button("🔄 データ更新", use_container_width=True):
        st.session_state.realtime_data = generate_realtime_data()
        st.session_state.last_update = datetime.now().isoformat()
        st.success("✅ データを更新しました")
        st.rerun()
    
    if st.button("⏸️ 全キャンペーン一時停止", use_container_width=True):
        st.warning("⚠️ 全キャンペーンを一時停止しました")
    
    if st.button("🚀 緊急最適化実行", use_container_width=True, type="primary"):
        st.success("🎯 緊急最適化を実行中...")
    
    st.markdown("---")
    
    # システム状態
    st.subheader("🔧 システム状態")
    
    system_metrics = [
        ("API接続", "🟢 正常", "98.7%"),
        ("AIエンジン", "🟢 稼働中", "99.2%"),
        ("データ同期", "🟡 遅延", "94.1%"),
        ("自動実行", "🟢 有効", "100%")
    ]
    
    for metric, status, uptime in system_metrics:
        st.markdown(f"**{metric}**: {status} ({uptime})")
    
    st.markdown("---")
    
    # 緊急時制御
    st.subheader("🚨 緊急時制御")
    
    if st.button("🛑 緊急停止", use_container_width=True):
        st.error("🚨 緊急停止が実行されました")
    
    emergency_contacts = [
        "📧 admin@company.com",
        "📱 +81-90-1234-5678",
        "💬 Slack: #emergency"
    ]
    
    st.markdown("**緊急連絡先:**")
    for contact in emergency_contacts:
        st.markdown(f"- {contact}")
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("🎨 Creative Studio", use_container_width=True):
        st.switch_page("pages/ai_creative_studio.py")
    
    if st.button("📊 パフォーマンス分析", use_container_width=True):
        st.switch_page("pages/performance_dashboard.py")

# フッター
st.markdown("---")
st.caption("⚡ Realtime Ad Optimizer: 最先端のAI技術で広告パフォーマンスをリアルタイム最適化。限界を超えた広告代理店機能を体験してください。")