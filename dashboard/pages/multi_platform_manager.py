#!/usr/bin/env python3
"""
マルチプラットフォーム統合広告管理システム
全プラットフォームの広告を一元管理・最適化
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

# ページ設定
st.set_page_config(
    page_title="マルチプラットフォーム広告管理",
    page_icon="🌐",
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
    .multiplatform-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .multiplatform-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, rgba(255,255,255,0.1), transparent, rgba(255,255,255,0.1));
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .multiplatform-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .multiplatform-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* プラットフォームカード */
    .platform-card {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .platform-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
        border-color: #667eea;
    }
    
    .platform-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .platform-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .platform-status {
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-warning {
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .status-paused {
        background: rgba(148, 163, 184, 0.2);
        color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    /* メトリクスグリッド */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .metric-item {
        background: rgba(30, 41, 59, 0.6);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s;
    }
    
    .metric-item:hover {
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateY(-3px);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 5px;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    .metric-change {
        font-size: 0.7rem;
        padding: 2px 6px;
        border-radius: 10px;
        margin-top: 5px;
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
    
    /* 統合ダッシュボード */
    .unified-dashboard {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
    }
    
    .dashboard-title {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* クロスプラットフォームメトリクス */
    .cross-platform-metric {
        background: rgba(30, 41, 59, 0.8);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s;
    }
    
    .cross-platform-metric:hover {
        border-color: rgba(102, 126, 234, 0.6);
        transform: translateY(-5px);
    }
    
    .cross-metric-value {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    .cross-metric-label {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    
    .cross-metric-detail {
        color: #e2e8f0;
        font-size: 0.9rem;
    }
    
    /* アクションセンター */
    .action-center {
        background: rgba(30, 41, 59, 0.6);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 20px 0;
    }
    
    .action-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        text-align: center;
    }
    
    .action-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    .action-urgent {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .action-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    /* 同期ステータス */
    .sync-status {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 15px;
        background: rgba(30, 41, 59, 0.6);
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .sync-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: syncPulse 2s infinite;
    }
    
    .sync-active {
        background: #10b981;
    }
    
    .sync-error {
        background: #ef4444;
    }
    
    .sync-warning {
        background: #f59e0b;
    }
    
    @keyframes syncPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    
    /* プラットフォーム比較チャート */
    .comparison-chart {
        background: rgba(30, 41, 59, 0.5);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 20px 0;
    }
    
    /* 自動化ルール */
    .automation-rule {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 15px 0;
        transition: all 0.3s;
    }
    
    .automation-rule:hover {
        background: rgba(30, 41, 59, 0.8);
        transform: translateX(5px);
    }
    
    .rule-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .rule-name {
        font-weight: bold;
        color: #667eea;
    }
    
    .rule-trigger {
        background: rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 4px 8px;
        border-radius: 8px;
        font-size: 0.8rem;
    }
    
    /* 予算配分 */
    .budget-allocation {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 20px 0;
    }
    
    .allocation-bar {
        display: flex;
        height: 40px;
        border-radius: 20px;
        overflow: hidden;
        margin: 15px 0;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    .allocation-segment {
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    
    .allocation-segment:hover {
        filter: brightness(1.2);
        transform: scaleY(1.1);
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'platform_data' not in st.session_state:
    st.session_state.platform_data = {}

if 'cross_platform_campaigns' not in st.session_state:
    st.session_state.cross_platform_campaigns = {}

if 'automation_rules' not in st.session_state:
    st.session_state.automation_rules = []

def generate_platform_data():
    """プラットフォーム別データを生成"""
    platforms = {
        'Google Ads': {
            'icon': '🔍',
            'color': '#4285f4',
            'api_status': 'active',
            'campaigns': np.random.randint(15, 45),
            'daily_spend': np.random.uniform(15000, 50000),
            'impressions': np.random.randint(50000, 200000),
            'clicks': np.random.randint(1500, 8000),
            'conversions': np.random.randint(80, 400),
            'ctr': np.random.uniform(2.1, 6.8),
            'cpc': np.random.uniform(200, 800),
            'cpa': np.random.uniform(3000, 12000),
            'roas': np.random.uniform(2.5, 8.2),
            'quality_score': np.random.uniform(6.5, 9.2)
        },
        'Facebook Ads': {
            'icon': '📘',
            'color': '#1877f2',
            'api_status': 'active',
            'campaigns': np.random.randint(12, 35),
            'daily_spend': np.random.uniform(8000, 35000),
            'impressions': np.random.randint(80000, 300000),
            'clicks': np.random.randint(2000, 12000),
            'conversions': np.random.randint(100, 600),
            'ctr': np.random.uniform(1.8, 5.5),
            'cpc': np.random.uniform(150, 600),
            'cpa': np.random.uniform(2500, 10000),
            'roas': np.random.uniform(3.0, 9.1),
            'relevance_score': np.random.uniform(7.2, 9.8)
        },
        'Instagram Ads': {
            'icon': '📷',
            'color': '#E4405F',
            'api_status': 'warning',
            'campaigns': np.random.randint(8, 25),
            'daily_spend': np.random.uniform(5000, 25000),
            'impressions': np.random.randint(60000, 250000),
            'clicks': np.random.randint(1800, 10000),
            'conversions': np.random.randint(70, 450),
            'ctr': np.random.uniform(2.2, 6.1),
            'cpc': np.random.uniform(180, 650),
            'cpa': np.random.uniform(2800, 9500),
            'roas': np.random.uniform(2.8, 7.9),
            'engagement_rate': np.random.uniform(4.5, 12.3)
        },
        'LinkedIn Ads': {
            'icon': '💼',
            'color': '#0077b5',
            'api_status': 'active',
            'campaigns': np.random.randint(5, 18),
            'daily_spend': np.random.uniform(3000, 18000),
            'impressions': np.random.randint(20000, 80000),
            'clicks': np.random.randint(400, 2500),
            'conversions': np.random.randint(25, 150),
            'ctr': np.random.uniform(0.8, 3.2),
            'cpc': np.random.uniform(800, 2500),
            'cpa': np.random.uniform(8000, 25000),
            'roas': np.random.uniform(1.8, 5.5),
            'lead_quality': np.random.uniform(7.5, 9.5)
        },
        'Twitter Ads': {
            'icon': '🐦',
            'color': '#1da1f2',
            'api_status': 'error',
            'campaigns': np.random.randint(3, 12),
            'daily_spend': np.random.uniform(2000, 12000),
            'impressions': np.random.randint(30000, 120000),
            'clicks': np.random.randint(600, 3500),
            'conversions': np.random.randint(15, 80),
            'ctr': np.random.uniform(1.2, 4.1),
            'cpc': np.random.uniform(300, 1200),
            'cpa': np.random.uniform(5000, 18000),
            'roas': np.random.uniform(1.5, 4.8),
            'engagement_rate': np.random.uniform(2.1, 8.7)
        },
        'TikTok Ads': {
            'icon': '🎵',
            'color': '#ff0050',
            'api_status': 'active',
            'campaigns': np.random.randint(4, 15),
            'daily_spend': np.random.uniform(4000, 20000),
            'impressions': np.random.randint(100000, 400000),
            'clicks': np.random.randint(3000, 15000),
            'conversions': np.random.randint(120, 600),
            'ctr': np.random.uniform(3.5, 8.2),
            'cpc': np.random.uniform(120, 450),
            'cpa': np.random.uniform(2000, 7500),
            'roas': np.random.uniform(3.5, 10.2),
            'view_rate': np.random.uniform(45, 85)
        }
    }
    
    return platforms

def calculate_cross_platform_metrics(platforms):
    """クロスプラットフォーム統合メトリクスを計算"""
    total_spend = sum(p['daily_spend'] for p in platforms.values())
    total_impressions = sum(p['impressions'] for p in platforms.values())
    total_clicks = sum(p['clicks'] for p in platforms.values())
    total_conversions = sum(p['conversions'] for p in platforms.values())
    
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    avg_cpa = total_spend / total_conversions if total_conversions > 0 else 0
    total_roas = sum(p['roas'] * p['daily_spend'] for p in platforms.values()) / total_spend if total_spend > 0 else 0
    
    return {
        'total_spend': total_spend,
        'total_impressions': total_impressions,
        'total_clicks': total_clicks,
        'total_conversions': total_conversions,
        'avg_ctr': avg_ctr,
        'avg_cpc': avg_cpc,
        'avg_cpa': avg_cpa,
        'total_roas': total_roas,
        'active_campaigns': sum(p['campaigns'] for p in platforms.values())
    }

# データ生成
platform_data = generate_platform_data()
cross_metrics = calculate_cross_platform_metrics(platform_data)

# ヘッダー
st.markdown("""
<div class="multiplatform-header">
    <div class="multiplatform-title">🌐 マルチプラットフォーム統合管理</div>
    <div class="multiplatform-subtitle">全プラットフォームの広告を一元管理・最適化する究極のソリューション</div>
</div>
""", unsafe_allow_html=True)

# 統合ダッシュボード
st.markdown("""
<div class="unified-dashboard">
    <div class="dashboard-title">📊 統合パフォーマンスダッシュボード</div>
</div>
""", unsafe_allow_html=True)

# 統合メトリクス
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="cross-platform-metric">
        <div class="cross-metric-value">¥{cross_metrics['total_spend']:,.0f}</div>
        <div class="cross-metric-label">総広告費</div>
        <div class="cross-metric-detail">6プラットフォーム合計</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="cross-platform-metric">
        <div class="cross-metric-value">{cross_metrics['total_impressions']:,}</div>
        <div class="cross-metric-label">総インプレッション</div>
        <div class="cross-metric-detail">リーチ最大化</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="cross-platform-metric">
        <div class="cross-metric-value">{cross_metrics['avg_ctr']:.2f}%</div>
        <div class="cross-metric-label">統合CTR</div>
        <div class="cross-metric-detail">加重平均</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="cross-platform-metric">
        <div class="cross-metric-value">{cross_metrics['total_conversions']:,}</div>
        <div class="cross-metric-label">総コンバージョン</div>
        <div class="cross-metric-detail">全プラットフォーム</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="cross-platform-metric">
        <div class="cross-metric-value">{cross_metrics['total_roas']:.1f}x</div>
        <div class="cross-metric-label">統合ROAS</div>
        <div class="cross-metric-detail">収益性指標</div>
    </div>
    """, unsafe_allow_html=True)

# タブ構成
tabs = st.tabs(["🎛️ プラットフォーム管理", "📊 比較分析", "🤖 自動化ルール", "💰 予算最適化", "🔄 クロスプラットフォームキャンペーン"])

# プラットフォーム管理タブ
with tabs[0]:
    st.markdown("### 🎛️ プラットフォーム別管理コンソール")
    
    # プラットフォーム一覧
    for platform_name, data in platform_data.items():
        
        # ステータス決定
        status_map = {
            'active': ('status-active', '🟢 稼働中'),
            'warning': ('status-warning', '🟡 要注意'),
            'error': ('status-error', '🔴 エラー'),
            'paused': ('status-paused', '⏸️ 停止中')
        }
        
        status_class, status_text = status_map[data['api_status']]
        
        st.markdown(f"""
        <div class="platform-card">
            <div class="platform-header">
                <div class="platform-name">
                    {data['icon']} {platform_name}
                </div>
                <div class="platform-status {status_class}">
                    {status_text}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # メトリクスグリッド
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        metrics = [
            (col1, "キャンペーン数", f"{data['campaigns']}", "+3"),
            (col2, "日別広告費", f"¥{data['daily_spend']:,.0f}", "+12%"),
            (col3, "CTR", f"{data['ctr']:.2f}%", "+0.3%"),
            (col4, "CPC", f"¥{data['cpc']:.0f}", "-5%"),
            (col5, "CPA", f"¥{data['cpa']:,.0f}", "-8%"),
            (col6, "ROAS", f"{data['roas']:.1f}x", "+0.2x")
        ]
        
        for col, label, value, change in metrics:
            with col:
                change_class = "change-positive" if change.startswith('+') or change.startswith('-') and 'CPC' in label or 'CPA' in label else "change-negative"
                if 'CPC' in label or 'CPA' in label:
                    change_class = "change-positive" if change.startswith('-') else "change-negative"
                
                st.markdown(f"""
                <div class="metric-item">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-change {change_class}">{change}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # アクションボタン
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button(f"📊 詳細分析", key=f"analyze_{platform_name}"):
                st.info(f"{platform_name}の詳細分析画面を開きます")
        
        with action_col2:
            if st.button(f"⚙️ 設定変更", key=f"settings_{platform_name}"):
                st.info(f"{platform_name}の設定画面を開きます")
        
        with action_col3:
            action_text = "⏸️ 一時停止" if data['api_status'] == 'active' else "▶️ 再開"
            if st.button(action_text, key=f"toggle_{platform_name}"):
                new_status = "paused" if data['api_status'] == 'active' else "active"
                st.success(f"{platform_name}を{new_status}に変更しました")
        
        with action_col4:
            if st.button(f"🔄 同期", key=f"sync_{platform_name}"):
                st.success(f"{platform_name}との同期を開始しました")
        
        # 同期ステータス
        sync_statuses = ['sync-active', 'sync-warning', 'sync-error']
        sync_labels = ['同期中', '同期遅延', '同期エラー']
        sync_idx = hash(platform_name) % 3
        
        st.markdown(f"""
        <div class="sync-status">
            <div class="sync-indicator {sync_statuses[sync_idx]}"></div>
            <span>API同期ステータス: {sync_labels[sync_idx]}</span>
            <span style="margin-left: auto; color: #94a3b8;">最終同期: {(datetime.now() - timedelta(minutes=np.random.randint(1, 30))).strftime('%H:%M')}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

# 比較分析タブ
with tabs[1]:
    st.markdown("### 📊 プラットフォーム比較分析")
    
    # メトリクス選択
    col1, col2 = st.columns(2)
    
    with col1:
        comparison_metric = st.selectbox(
            "比較メトリクス",
            ["CTR", "CPC", "CPA", "ROAS", "インプレッション", "コンバージョン数"]
        )
    
    with col2:
        chart_type = st.selectbox(
            "グラフタイプ",
            ["棒グラフ", "レーダーチャート", "散布図", "ヒートマップ"]
        )
    
    # データ準備
    platforms = list(platform_data.keys())
    metric_mapping = {
        "CTR": "ctr",
        "CPC": "cpc", 
        "CPA": "cpa",
        "ROAS": "roas",
        "インプレッション": "impressions",
        "コンバージョン数": "conversions"
    }
    
    metric_key = metric_mapping[comparison_metric]
    values = [platform_data[p][metric_key] for p in platforms]
    colors = [platform_data[p]['color'] for p in platforms]
    
    # グラフ表示
    if chart_type == "棒グラフ":
        fig = px.bar(
            x=platforms,
            y=values,
            color=values,
            color_continuous_scale="Viridis",
            title=f"プラットフォーム別{comparison_metric}比較"
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "レーダーチャート":
        # 複数メトリクスのレーダーチャート
        metrics_for_radar = ["ctr", "roas", "impressions", "conversions"]
        metric_names = ["CTR", "ROAS", "インプレッション", "コンバージョン"]
        
        fig = go.Figure()
        
        for platform in platforms[:3]:  # 上位3プラットフォーム
            values_normalized = []
            for metric in metrics_for_radar:
                max_val = max(platform_data[p][metric] for p in platforms)
                normalized = platform_data[platform][metric] / max_val * 100
                values_normalized.append(normalized)
            
            fig.add_trace(go.Scatterpolar(
                r=values_normalized + [values_normalized[0]],  # 閉じるため最初の値を追加
                theta=metric_names + [metric_names[0]],
                fill='toself',
                name=platform,
                line=dict(color=platform_data[platform]['color'])
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="プラットフォーム別パフォーマンスレーダー",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "散布図":
        # CTR vs ROAS の散布図
        ctr_values = [platform_data[p]['ctr'] for p in platforms]
        roas_values = [platform_data[p]['roas'] for p in platforms]
        spend_values = [platform_data[p]['daily_spend'] for p in platforms]
        
        fig = px.scatter(
            x=ctr_values,
            y=roas_values,
            size=spend_values,
            color=platforms,
            hover_name=platforms,
            labels={'x': 'CTR (%)', 'y': 'ROAS (x)'},
            title="CTR vs ROAS (バブルサイズ = 広告費)"
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # パフォーマンスランキング
    st.markdown("### 🏆 パフォーマンスランキング")
    
    ranking_metric = st.selectbox("ランキング基準", ["ROAS", "CTR", "コンバージョン数", "効率スコア"])
    
    if ranking_metric == "効率スコア":
        # 独自の効率スコア計算
        efficiency_scores = {}
        for platform, data in platform_data.items():
            score = (data['roas'] * 0.4 + data['ctr'] * 0.3 + (10000/data['cpa']) * 0.3) * 10
            efficiency_scores[platform] = score
        
        sorted_platforms = sorted(efficiency_scores.items(), key=lambda x: x[1], reverse=True)
    else:
        metric_key = metric_mapping[ranking_metric]
        sorted_platforms = sorted(platform_data.items(), key=lambda x: x[1][metric_key], reverse=True)
        sorted_platforms = [(name, data[metric_key]) for name, data in sorted_platforms]
    
    for i, (platform, score) in enumerate(sorted_platforms, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}位"
        
        st.markdown(f"""
        <div class="platform-card" style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 1.5rem;">{medal}</span>
                    <span style="font-size: 1.2rem; font-weight: bold;">{platform_data[platform]['icon']} {platform}</span>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">
                        {f'{score:.2f}' if isinstance(score, float) else score}
                    </div>
                    <div style="color: #94a3b8;">{ranking_metric}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 自動化ルールタブ
with tabs[2]:
    st.markdown("### 🤖 クロスプラットフォーム自動化ルール")
    
    # 新規ルール作成
    with st.expander("➕ 新しい自動化ルールを作成"):
        with st.form("automation_rule_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                rule_name = st.text_input("ルール名*", placeholder="CTR低下時の入札調整")
                trigger_platform = st.multiselect(
                    "対象プラットフォーム",
                    list(platform_data.keys()),
                    default=list(platform_data.keys())[:2]
                )
                trigger_metric = st.selectbox("トリガーメトリクス", ["CTR", "CPC", "CPA", "ROAS", "コンバージョン数"])
            
            with col2:
                trigger_condition = st.selectbox("条件", ["より小さい", "より大きい", "等しい", "変化率"])
                trigger_value = st.number_input("閾値", value=2.0, step=0.1)
                trigger_duration = st.selectbox("持続時間", ["即座に", "15分間", "1時間", "6時間", "24時間"])
            
            action_type = st.selectbox(
                "実行アクション",
                ["入札価格調整", "予算再配分", "キャンペーン一時停止", "アラート送信", "クリエイティブ変更"]
            )
            
            action_details = st.text_area(
                "アクション詳細",
                placeholder="例: 入札価格を15%削減し、高パフォーマンスキーワードに予算を集中"
            )
            
            if st.form_submit_button("🚀 ルールを作成", type="primary"):
                if rule_name and trigger_platform:
                    new_rule = {
                        'id': str(uuid.uuid4()),
                        'name': rule_name,
                        'platforms': trigger_platform,
                        'trigger': {
                            'metric': trigger_metric,
                            'condition': trigger_condition,
                            'value': trigger_value,
                            'duration': trigger_duration
                        },
                        'action': {
                            'type': action_type,
                            'details': action_details
                        },
                        'created_at': datetime.now().isoformat(),
                        'status': 'active',
                        'executions': 0
                    }
                    
                    st.session_state.automation_rules.append(new_rule)
                    st.success(f"✅ 自動化ルール '{rule_name}' を作成しました！")
                    st.rerun()
                else:
                    st.error("必須項目を入力してください")
    
    # 既存ルール一覧
    st.markdown("### 📋 アクティブな自動化ルール")
    
    if st.session_state.automation_rules:
        for rule in st.session_state.automation_rules:
            platforms_text = ", ".join(rule['platforms'])
            trigger = rule['trigger']
            action = rule['action']
            
            status_color = "#10b981" if rule['status'] == 'active' else "#94a3b8"
            
            st.markdown(f"""
            <div class="automation-rule">
                <div class="rule-header">
                    <span class="rule-name">{rule['name']}</span>
                    <span class="rule-trigger" style="background: rgba(102, 126, 234, 0.2);">
                        {trigger['metric']} {trigger['condition']} {trigger['value']}
                    </span>
                </div>
                <div style="margin: 10px 0;">
                    <strong>対象:</strong> {platforms_text}<br>
                    <strong>アクション:</strong> {action['type']}<br>
                    <strong>詳細:</strong> {action['details']}<br>
                    <strong>実行回数:</strong> {rule['executions']}回
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"✏️ 編集", key=f"edit_rule_{rule['id']}"):
                    st.info(f"ルール '{rule['name']}' の編集画面を開きます")
            
            with col2:
                status_text = "⏸️ 無効化" if rule['status'] == 'active' else "▶️ 有効化"
                if st.button(status_text, key=f"toggle_rule_{rule['id']}"):
                    rule['status'] = 'inactive' if rule['status'] == 'active' else 'active'
                    st.success(f"ルールステータスを変更しました")
                    st.rerun()
            
            with col3:
                if st.button(f"🗑️ 削除", key=f"delete_rule_{rule['id']}"):
                    st.session_state.automation_rules.remove(rule)
                    st.success(f"ルール '{rule['name']}' を削除しました")
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info("まだ自動化ルールが作成されていません。上記のフォームから作成してください。")
    
    # プリセットルール
    st.markdown("### 🎯 プリセット自動化ルール")
    
    preset_rules = [
        {
            "name": "緊急CPA上昇対応",
            "description": "CPAが目標値を30%上回った場合、自動的に入札価格を調整",
            "complexity": "高"
        },
        {
            "name": "週末予算最適化",
            "description": "週末のパフォーマンス低下時に予算をウィークデイにシフト",
            "complexity": "中"
        },
        {
            "name": "競合対応入札調整",
            "description": "インプレッションシェア低下時の自動入札アップ",
            "complexity": "中"
        },
        {
            "name": "品質スコア最適化",
            "description": "品質スコア低下キーワードの自動一時停止",
            "complexity": "低"
        }
    ]
    
    for preset in preset_rules:
        complexity_color = {"高": "#ef4444", "中": "#f59e0b", "低": "#10b981"}[preset['complexity']]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h4 style="color: #667eea; margin-bottom: 8px;">{preset['name']}</h4>
                <p style="margin-bottom: 8px;">{preset['description']}</p>
                <span style="background: {complexity_color}; color: white; padding: 4px 8px; border-radius: 8px; font-size: 0.8rem;">
                    複雑度: {preset['complexity']}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"📥 インポート", key=f"import_{preset['name']}"):
                st.success(f"✅ '{preset['name']}' をインポートしました！")

# 予算最適化タブ
with tabs[3]:
    st.markdown("### 💰 予算最適化ダッシュボード")
    
    # 現在の予算配分
    st.markdown("#### 📊 現在の予算配分")
    
    total_budget = sum(data['daily_spend'] for data in platform_data.values())
    
    # 予算配分可視化
    allocation_data = []
    colors_list = []
    
    for platform, data in platform_data.items():
        percentage = (data['daily_spend'] / total_budget) * 100
        allocation_data.append(percentage)
        colors_list.append(data['color'])
    
    # HTML for allocation bar
    allocation_html = '<div class="allocation-bar">'
    for i, (platform, percentage) in enumerate(zip(platform_data.keys(), allocation_data)):
        allocation_html += f'''
        <div class="allocation-segment" style="width: {percentage}%; background: {colors_list[i]};">
            {platform[:4]} {percentage:.0f}%
        </div>
        '''
    allocation_html += '</div>'
    
    st.markdown(f"""
    <div class="budget-allocation">
        <h4>💰 日別予算配分 (総額: ¥{total_budget:,.0f})</h4>
        {allocation_html}
    </div>
    """, unsafe_allow_html=True)
    
    # 予算最適化推奨
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 AI最適化推奨")
        
        # ROAS基準の最適化推奨
        platform_roas = [(name, data['roas']) for name, data in platform_data.items()]
        platform_roas.sort(key=lambda x: x[1], reverse=True)
        
        best_performer = platform_roas[0]
        worst_performer = platform_roas[-1]
        
        optimizations = [
            {
                "type": "予算再配分",
                "description": f"{best_performer[0]} (ROAS {best_performer[1]:.1f}x) への予算追加を推奨",
                "impact": "+23% ROI向上",
                "urgency": "high"
            },
            {
                "type": "予算削減",
                "description": f"{worst_performer[0]} (ROAS {worst_performer[1]:.1f}x) の予算を削減",
                "impact": "¥12,000 コスト削減",
                "urgency": "medium"
            },
            {
                "type": "時間帯最適化",
                "description": "高パフォーマンス時間帯への予算集中",
                "impact": "+18% CTR改善",
                "urgency": "low"
            }
        ]
        
        for opt in optimizations:
            urgency_color = {"high": "#ef4444", "medium": "#f59e0b", "low": "#10b981"}[opt['urgency']]
            
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid {urgency_color};">
                <h5 style="color: #667eea; margin-bottom: 8px;">{opt['type']}</h5>
                <p style="margin-bottom: 8px;">{opt['description']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 4px 8px; border-radius: 8px; font-size: 0.8rem;">
                        {opt['impact']}
                    </span>
                    <span style="color: {urgency_color}; font-size: 0.8rem; font-weight: bold;">
                        {opt['urgency'].upper()}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ⚙️ 予算調整シミュレーター")
        
        # 予算調整シミュレーション
        st.markdown("**予算を移動:**")
        
        source_platform = st.selectbox("移動元プラットフォーム", list(platform_data.keys()))
        target_platform = st.selectbox("移動先プラットフォーム", list(platform_data.keys()))
        move_amount = st.slider("移動金額 (¥)", 1000, 20000, 5000, 1000)
        
        if source_platform != target_platform:
            # シミュレーション結果
            source_current = platform_data[source_platform]['daily_spend']
            target_current = platform_data[target_platform]['daily_spend']
            source_roas = platform_data[source_platform]['roas']
            target_roas = platform_data[target_platform]['roas']
            
            # 予想効果計算
            lost_revenue = move_amount * source_roas
            gained_revenue = move_amount * target_roas
            net_impact = gained_revenue - lost_revenue
            
            impact_color = "#10b981" if net_impact > 0 else "#ef4444"
            impact_text = f"+¥{net_impact:,.0f}" if net_impact > 0 else f"¥{net_impact:,.0f}"
            
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 15px; border: 1px solid rgba(102, 126, 234, 0.3);">
                <h5 style="color: #667eea; margin-bottom: 15px;">シミュレーション結果</h5>
                
                <div style="margin-bottom: 15px;">
                    <strong>{source_platform}:</strong> ¥{source_current:,.0f} → ¥{source_current - move_amount:,.0f}<br>
                    <strong>{target_platform}:</strong> ¥{target_current:,.0f} → ¥{target_current + move_amount:,.0f}
                </div>
                
                <div style="padding: 15px; background: rgba(30, 41, 59, 0.8); border-radius: 10px; text-align: center;">
                    <div style="color: {impact_color}; font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;">
                        {impact_text}
                    </div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">
                        予想収益への影響 (日別)
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 変更を適用", type="primary"):
                st.success(f"✅ 予算配分を変更しました！\n{source_platform} から {target_platform} に ¥{move_amount:,} を移動")
    
    # 予算パフォーマンス履歴
    st.markdown("#### 📈 予算パフォーマンス履歴")
    
    # サンプル履歴データ
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    budget_history = pd.DataFrame({
        'date': dates,
        'total_spend': np.random.uniform(80000, 120000, 30),
        'total_revenue': np.random.uniform(200000, 400000, 30),
        'roas': np.random.uniform(2.5, 4.2, 30)
    })
    
    fig_budget = go.Figure()
    
    fig_budget.add_trace(go.Scatter(
        x=budget_history['date'],
        y=budget_history['total_spend'],
        mode='lines+markers',
        name='広告費',
        line=dict(color='#ef4444', width=2),
        yaxis='y'
    ))
    
    fig_budget.add_trace(go.Scatter(
        x=budget_history['date'],
        y=budget_history['total_revenue'],
        mode='lines+markers',
        name='収益',
        line=dict(color='#10b981', width=2),
        yaxis='y2'
    ))
    
    fig_budget.update_layout(
        title="予算と収益の推移",
        xaxis_title="日付",
        yaxis=dict(title="広告費 (¥)", side="left"),
        yaxis2=dict(title="収益 (¥)", side="right", overlaying="y"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_budget, use_container_width=True)

# クロスプラットフォームキャンペーンタブ
with tabs[4]:
    st.markdown("### 🔄 クロスプラットフォームキャンペーン")
    
    # 新規キャンペーン作成
    with st.expander("🚀 新規クロスプラットフォームキャンペーンを作成"):
        with st.form("cross_campaign_form"):
            campaign_name = st.text_input("キャンペーン名*", placeholder="例: 新製品ローンチキャンペーン")
            
            col1, col2 = st.columns(2)
            
            with col1:
                target_platforms = st.multiselect(
                    "配信プラットフォーム*",
                    list(platform_data.keys()),
                    default=list(platform_data.keys())[:3]
                )
                campaign_objective = st.selectbox(
                    "キャンペーン目標",
                    ["ブランド認知", "トラフィック獲得", "リード生成", "売上向上", "アプリインストール"]
                )
                total_budget = st.number_input("総予算 (¥)", min_value=10000, value=100000, step=10000)
            
            with col2:
                campaign_duration = st.number_input("期間 (日)", min_value=1, value=14, step=1)
                target_audience = st.text_input("ターゲットオーディエンス", placeholder="例: 25-35歳 マーケティング担当者")
                priority_metric = st.selectbox("優先最適化メトリクス", ["CTR", "CPC", "CPA", "ROAS"])
            
            creative_assets = st.text_area(
                "クリエイティブ素材",
                placeholder="画像: campaign_banner.jpg\n動画: product_demo.mp4\nコピー: 革新的なマーケティングツール"
            )
            
            if st.form_submit_button("🎯 キャンペーンを作成", type="primary"):
                if campaign_name and target_platforms:
                    # 予算配分計算
                    platform_weights = {p: platform_data[p]['roas'] for p in target_platforms}
                    total_weight = sum(platform_weights.values())
                    budget_allocation = {p: (weight/total_weight) * total_budget for p, weight in platform_weights.items()}
                    
                    new_campaign = {
                        'id': str(uuid.uuid4()),
                        'name': campaign_name,
                        'platforms': target_platforms,
                        'objective': campaign_objective,
                        'total_budget': total_budget,
                        'budget_allocation': budget_allocation,
                        'duration': campaign_duration,
                        'target_audience': target_audience,
                        'priority_metric': priority_metric,
                        'creative_assets': creative_assets,
                        'created_at': datetime.now().isoformat(),
                        'status': 'draft',
                        'performance': {
                            'impressions': 0,
                            'clicks': 0,
                            'conversions': 0,
                            'spend': 0
                        }
                    }
                    
                    st.session_state.cross_platform_campaigns[new_campaign['id']] = new_campaign
                    st.success(f"✅ クロスプラットフォームキャンペーン '{campaign_name}' を作成しました！")
                    st.rerun()
                else:
                    st.error("必須項目を入力してください")
    
    # 既存キャンペーン一覧
    st.markdown("### 📋 アクティブキャンペーン")
    
    if st.session_state.cross_platform_campaigns:
        for campaign_id, campaign in st.session_state.cross_platform_campaigns.items():
            # ステータスに応じたスタイル
            status_styles = {
                'draft': ('status-paused', '📝 下書き'),
                'active': ('status-active', '🟢 配信中'),
                'paused': ('status-warning', '⏸️ 一時停止'),
                'completed': ('status-active', '✅ 完了')
            }
            
            status_class, status_text = status_styles.get(campaign['status'], ('status-paused', campaign['status']))
            
            st.markdown(f"""
            <div class="platform-card">
                <div class="platform-header">
                    <div class="platform-name">
                        🔄 {campaign['name']}
                    </div>
                    <div class="platform-status {status_class}">
                        {status_text}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # キャンペーン詳細
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**基本情報:**")
                st.write(f"• 目標: {campaign['objective']}")
                st.write(f"• 期間: {campaign['duration']}日間")
                st.write(f"• 総予算: ¥{campaign['total_budget']:,}")
                st.write(f"• プラットフォーム: {len(campaign['platforms'])}個")
            
            with col2:
                st.markdown("**予算配分:**")
                for platform, budget in campaign['budget_allocation'].items():
                    percentage = (budget / campaign['total_budget']) * 100
                    st.write(f"• {platform}: ¥{budget:,.0f} ({percentage:.0f}%)")
            
            with col3:
                st.markdown("**パフォーマンス:**")
                perf = campaign['performance']
                st.write(f"• インプレッション: {perf['impressions']:,}")
                st.write(f"• クリック: {perf['clicks']:,}")
                st.write(f"• コンバージョン: {perf['conversions']:,}")
                st.write(f"• 消化予算: ¥{perf['spend']:,}")
            
            # アクションボタン
            action_col1, action_col2, action_col3, action_col4 = st.columns(4)
            
            with action_col1:
                if campaign['status'] == 'draft':
                    if st.button(f"🚀 配信開始", key=f"start_{campaign_id}"):
                        campaign['status'] = 'active'
                        st.success(f"✅ '{campaign['name']}' の配信を開始しました！")
                        st.rerun()
                elif campaign['status'] == 'active':
                    if st.button(f"⏸️ 一時停止", key=f"pause_{campaign_id}"):
                        campaign['status'] = 'paused'
                        st.success(f"⏸️ '{campaign['name']}' を一時停止しました")
                        st.rerun()
                else:
                    if st.button(f"▶️ 再開", key=f"resume_{campaign_id}"):
                        campaign['status'] = 'active'
                        st.success(f"▶️ '{campaign['name']}' を再開しました")
                        st.rerun()
            
            with action_col2:
                if st.button(f"📊 詳細分析", key=f"analyze_campaign_{campaign_id}"):
                    st.info(f"'{campaign['name']}' の詳細分析を表示します")
            
            with action_col3:
                if st.button(f"✏️ 編集", key=f"edit_campaign_{campaign_id}"):
                    st.info(f"'{campaign['name']}' の編集画面を開きます")
            
            with action_col4:
                if st.button(f"📋 複製", key=f"clone_campaign_{campaign_id}"):
                    cloned_campaign = campaign.copy()
                    cloned_campaign['id'] = str(uuid.uuid4())
                    cloned_campaign['name'] = f"{campaign['name']} (コピー)"
                    cloned_campaign['status'] = 'draft'
                    cloned_campaign['created_at'] = datetime.now().isoformat()
                    
                    st.session_state.cross_platform_campaigns[cloned_campaign['id']] = cloned_campaign
                    st.success(f"✅ キャンペーンを複製しました！")
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info("まだクロスプラットフォームキャンペーンが作成されていません。上記のフォームから作成してください。")
    
    # キャンペーンパフォーマンス比較
    if st.session_state.cross_platform_campaigns:
        st.markdown("### 📊 キャンペーンパフォーマンス比較")
        
        # サンプルデータ（実際にはDBから取得）
        campaign_comparison = []
        for campaign in st.session_state.cross_platform_campaigns.values():
            if campaign['status'] in ['active', 'completed']:
                # サンプルパフォーマンス生成
                impressions = np.random.randint(10000, 100000)
                clicks = np.random.randint(200, 3000)
                conversions = np.random.randint(20, 150)
                
                campaign_comparison.append({
                    'campaign': campaign['name'][:20] + "..." if len(campaign['name']) > 20 else campaign['name'],
                    'platforms': len(campaign['platforms']),
                    'impressions': impressions,
                    'clicks': clicks,
                    'conversions': conversions,
                    'ctr': (clicks / impressions) * 100,
                    'cvr': (conversions / clicks) * 100 if clicks > 0 else 0
                })
        
        if campaign_comparison:
            df_comparison = pd.DataFrame(campaign_comparison)
            
            # メトリクス選択
            comparison_metric = st.selectbox(
                "比較メトリクス",
                ["CTR", "CVR", "インプレッション", "クリック数", "コンバージョン数"],
                key="campaign_comparison_metric"
            )
            
            metric_map = {
                "CTR": "ctr",
                "CVR": "cvr", 
                "インプレッション": "impressions",
                "クリック数": "clicks",
                "コンバージョン数": "conversions"
            }
            
            fig_comparison = px.bar(
                df_comparison,
                x='campaign',
                y=metric_map[comparison_metric],
                color=metric_map[comparison_metric],
                color_continuous_scale="Viridis",
                title=f"キャンペーン別{comparison_metric}比較"
            )
            
            fig_comparison.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)

# サイドバー
with st.sidebar:
    st.header("🌐 マルチプラットフォーム管理")
    
    # 全体制御
    st.subheader("🎛️ 全体制御")
    
    if st.button("🔄 全プラットフォーム同期", use_container_width=True):
        st.success("✅ 全プラットフォームとの同期を開始しました")
    
    if st.button("⏸️ 全キャンペーン一時停止", use_container_width=True):
        st.warning("⚠️ 全キャンペーンを一時停止しました")
    
    if st.button("🚀 予算最適化実行", use_container_width=True, type="primary"):
        st.success("🎯 AI予算最適化を実行中...")
    
    st.markdown("---")
    
    # プラットフォーム接続状況
    st.subheader("🔗 API接続状況")
    
    for platform, data in platform_data.items():
        status_icon = {
            'active': '🟢',
            'warning': '🟡', 
            'error': '🔴',
            'paused': '⚪'
        }[data['api_status']]
        
        st.markdown(f"{status_icon} {data['icon']} {platform}")
    
    st.markdown("---")
    
    # 今日の統計
    st.subheader("📊 本日の統計")
    
    st.metric("アクティブキャンペーン", cross_metrics['active_campaigns'])
    st.metric("総インプレッション", f"{cross_metrics['total_impressions']:,}")
    st.metric("統合ROAS", f"{cross_metrics['total_roas']:.1f}x")
    
    # 効率ランキング
    st.subheader("🏆 プラットフォーム効率ランキング")
    
    efficiency_ranking = []
    for platform, data in platform_data.items():
        efficiency = data['roas'] * (data['ctr'] / 5) * (10000 / data['cpa'])
        efficiency_ranking.append((platform, efficiency))
    
    efficiency_ranking.sort(key=lambda x: x[1], reverse=True)
    
    for i, (platform, score) in enumerate(efficiency_ranking[:3], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        st.markdown(f"{medal} {platform_data[platform]['icon']} {platform}")
    
    st.markdown("---")
    
    # 緊急アラート
    st.subheader("🚨 アラート")
    
    alerts = [
        {"type": "error", "message": "Twitter API接続エラー", "time": "5分前"},
        {"type": "warning", "message": "Facebook予算90%消化", "time": "15分前"},
        {"type": "info", "message": "LinkedIn CTR向上中", "time": "1時間前"}
    ]
    
    for alert in alerts:
        alert_icon = {"error": "🔴", "warning": "🟡", "info": "🔵"}[alert['type']]
        st.markdown(f"{alert_icon} {alert['message']}")
        st.caption(alert['time'])
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("pages/../home.py")
    
    if st.button("⚡ リアルタイム最適化", use_container_width=True):
        st.switch_page("pages/realtime_ad_optimizer.py")
    
    if st.button("🎨 Creative Studio", use_container_width=True):
        st.switch_page("pages/ai_creative_studio.py")

# フッター
st.markdown("---")
st.caption("🌐 Multi-Platform Manager: 全プラットフォームを統合管理し、最大のROIを実現する次世代広告管理システム。限界を超えた効率化を体験してください。")