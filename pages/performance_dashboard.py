#!/usr/bin/env python3
"""
パフォーマンス追跡ダッシュボード
マーケティング施策のKPI監視と分析
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
from typing import Dict, List, Any

# ページ設定
st.set_page_config(
    page_title="パフォーマンスダッシュボード",
    page_icon="📈",
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
    
    /* KPIカード */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3b82f6;
        margin: 10px 0;
    }
    
    .kpi-label {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    
    .kpi-change {
        font-size: 0.9rem;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 10px;
    }
    
    .kpi-up {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .kpi-down {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    .kpi-neutral {
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
    }
    
    /* メトリクスグリッド */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    /* チャートコンテナ */
    .chart-container {
        background: rgba(30, 41, 59, 0.5);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin: 20px 0;
    }
    
    /* パフォーマンスインジケーター */
    .performance-indicator {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    
    .indicator-bar {
        flex-grow: 1;
        height: 8px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 4px;
        margin: 0 15px;
        position: relative;
    }
    
    .indicator-progress {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    /* アラートボックス */
    .alert-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    /* 時系列セレクター */
    .time-selector {
        background: rgba(30, 41, 59, 0.5);
        padding: 10px 20px;
        border-radius: 25px;
        display: inline-flex;
        gap: 10px;
        margin: 20px 0;
    }
    
    .time-option {
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .time-option:hover {
        background: rgba(59, 130, 246, 0.2);
    }
    
    .time-option.active {
        background: #3b82f6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'performance_data' not in st.session_state:
    st.session_state.performance_data = {}

if 'time_range' not in st.session_state:
    st.session_state.time_range = "7d"

def generate_sample_data(days: int = 30) -> pd.DataFrame:
    """サンプルパフォーマンスデータを生成"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # 基本的なトレンドを持つランダムデータ
    np.random.seed(42)
    base_traffic = 1000
    trend = np.linspace(0, 500, days)
    noise = np.random.normal(0, 100, days)
    
    data = {
        'date': dates,
        'traffic': (base_traffic + trend + noise).astype(int),
        'conversions': np.random.poisson(50 + trend/10, days),
        'revenue': np.random.exponential(1000, days) * (1 + trend/1000),
        'bounce_rate': 35 + np.random.normal(0, 5, days),
        'avg_session_duration': 180 + np.random.normal(0, 30, days),
        'social_engagement': np.random.poisson(200 + trend/5, days),
        'email_open_rate': 25 + np.random.normal(0, 3, days),
        'ctr': 3.5 + np.random.normal(0, 0.5, days)
    }
    
    return pd.DataFrame(data)

def calculate_kpi_change(current: float, previous: float) -> Dict[str, Any]:
    """KPIの変化率を計算"""
    if previous == 0:
        change = 0
    else:
        change = ((current - previous) / previous) * 100
    
    if change > 0:
        status = "up"
        symbol = "↑"
    elif change < 0:
        status = "down"
        symbol = "↓"
    else:
        status = "neutral"
        symbol = "→"
    
    return {
        "value": abs(change),
        "status": status,
        "symbol": symbol
    }

def get_time_range_data(df: pd.DataFrame, time_range: str) -> pd.DataFrame:
    """指定された期間のデータを取得"""
    days_map = {
        "24h": 1,
        "7d": 7,
        "30d": 30,
        "90d": 90
    }
    
    days = days_map.get(time_range, 7)
    cutoff_date = datetime.now() - timedelta(days=days)
    
    return df[df['date'] >= cutoff_date]

# データ準備
if 'sample_data' not in st.session_state:
    st.session_state.sample_data = generate_sample_data(90)

# ヘッダー
st.title("📈 パフォーマンス追跡ダッシュボード")
st.caption("マーケティング施策のリアルタイムKPI監視と分析")

# 時間範囲セレクター
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])

time_options = ["24h", "7d", "30d", "90d"]
for i, (col, option) in enumerate(zip([col1, col2, col3, col4], time_options)):
    with col:
        if st.button(
            option.upper(),
            key=f"time_{option}",
            type="primary" if st.session_state.time_range == option else "secondary",
            use_container_width=True
        ):
            st.session_state.time_range = option
            st.rerun()

# 現在の期間のデータを取得
current_data = get_time_range_data(st.session_state.sample_data, st.session_state.time_range)

# 主要KPI表示
st.markdown("### 🎯 主要KPI")

kpi_cols = st.columns(4)

# トラフィック
with kpi_cols[0]:
    current_traffic = current_data['traffic'].sum()
    avg_traffic = current_data['traffic'].mean()
    prev_traffic = st.session_state.sample_data['traffic'].iloc[-len(current_data)-1:-1].sum() if len(current_data) < len(st.session_state.sample_data) else current_traffic
    
    change = calculate_kpi_change(current_traffic, prev_traffic)
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">総トラフィック</div>
        <div class="kpi-value">{current_traffic:,}</div>
        <div class="kpi-change kpi-{change['status']}">
            {change['symbol']} {change['value']:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# コンバージョン
with kpi_cols[1]:
    current_conversions = current_data['conversions'].sum()
    conversion_rate = (current_conversions / current_traffic * 100) if current_traffic > 0 else 0
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">コンバージョン</div>
        <div class="kpi-value">{current_conversions:,}</div>
        <div class="kpi-change kpi-neutral">
            CVR: {conversion_rate:.2f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# 収益
with kpi_cols[2]:
    current_revenue = current_data['revenue'].sum()
    avg_order_value = current_revenue / current_conversions if current_conversions > 0 else 0
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">総収益</div>
        <div class="kpi-value">¥{current_revenue:,.0f}</div>
        <div class="kpi-change kpi-up">
            AOV: ¥{avg_order_value:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# エンゲージメント
with kpi_cols[3]:
    current_engagement = current_data['social_engagement'].sum()
    engagement_rate = current_engagement / current_traffic * 100 if current_traffic > 0 else 0
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">エンゲージメント</div>
        <div class="kpi-value">{current_engagement:,}</div>
        <div class="kpi-change kpi-up">
            Rate: {engagement_rate:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# チャートセクション
st.markdown("### 📊 パフォーマンストレンド")

# タブで異なるメトリクスを表示
chart_tabs = st.tabs(["トラフィック", "コンバージョン", "収益", "エンゲージメント", "詳細メトリクス"])

# トラフィックタブ
with chart_tabs[0]:
    fig_traffic = go.Figure()
    
    fig_traffic.add_trace(go.Scatter(
        x=current_data['date'],
        y=current_data['traffic'],
        mode='lines+markers',
        name='トラフィック',
        line=dict(color='#3b82f6', width=3),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))
    
    fig_traffic.update_layout(
        title="日別トラフィック推移",
        xaxis_title="日付",
        yaxis_title="訪問者数",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_traffic, use_container_width=True)
    
    # トラフィックソース分析
    st.markdown("#### トラフィックソース")
    
    source_data = pd.DataFrame({
        'ソース': ['検索', 'ソーシャル', 'ダイレクト', 'リファラル', 'メール'],
        '訪問者数': [
            int(current_traffic * 0.35),
            int(current_traffic * 0.25),
            int(current_traffic * 0.20),
            int(current_traffic * 0.15),
            int(current_traffic * 0.05)
        ]
    })
    
    fig_source = px.pie(
        source_data,
        values='訪問者数',
        names='ソース',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig_source.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_source, use_container_width=True)

# コンバージョンタブ
with chart_tabs[1]:
    fig_conversion = go.Figure()
    
    # コンバージョン数
    fig_conversion.add_trace(go.Bar(
        x=current_data['date'],
        y=current_data['conversions'],
        name='コンバージョン数',
        marker_color='#10b981',
        yaxis='y'
    ))
    
    # コンバージョン率
    cvr = (current_data['conversions'] / current_data['traffic'] * 100).fillna(0)
    fig_conversion.add_trace(go.Scatter(
        x=current_data['date'],
        y=cvr,
        mode='lines+markers',
        name='CVR (%)',
        line=dict(color='#f59e0b', width=2),
        yaxis='y2'
    ))
    
    fig_conversion.update_layout(
        title="コンバージョン推移",
        xaxis_title="日付",
        yaxis=dict(title="コンバージョン数", side="left"),
        yaxis2=dict(title="CVR (%)", side="right", overlaying="y"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_conversion, use_container_width=True)
    
    # ファネル分析
    st.markdown("#### コンバージョンファネル")
    
    funnel_data = pd.DataFrame({
        'ステージ': ['訪問', '商品閲覧', 'カート追加', '購入完了'],
        'ユーザー数': [
            current_traffic,
            int(current_traffic * 0.6),
            int(current_traffic * 0.3),
            current_conversions
        ]
    })
    
    fig_funnel = px.funnel(
        funnel_data,
        x='ユーザー数',
        y='ステージ',
        color_discrete_sequence=['#3b82f6']
    )
    
    fig_funnel.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)

# 収益タブ
with chart_tabs[2]:
    fig_revenue = go.Figure()
    
    # 日別収益
    fig_revenue.add_trace(go.Bar(
        x=current_data['date'],
        y=current_data['revenue'],
        name='収益',
        marker_color='#8b5cf6'
    ))
    
    # 累積収益
    cumulative_revenue = current_data['revenue'].cumsum()
    fig_revenue.add_trace(go.Scatter(
        x=current_data['date'],
        y=cumulative_revenue,
        mode='lines',
        name='累積収益',
        line=dict(color='#10b981', width=3, dash='dash')
    ))
    
    fig_revenue.update_layout(
        title="収益推移",
        xaxis_title="日付",
        yaxis_title="収益 (¥)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # 収益内訳
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### カテゴリ別収益")
        category_revenue = pd.DataFrame({
            'カテゴリ': ['製品A', '製品B', '製品C', 'その他'],
            '収益': [
                current_revenue * 0.4,
                current_revenue * 0.3,
                current_revenue * 0.2,
                current_revenue * 0.1
            ]
        })
        
        fig_category = px.pie(
            category_revenue,
            values='収益',
            names='カテゴリ',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig_category.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        st.markdown("#### ROI指標")
        
        # ROI計算（仮想データ）
        ad_spend = current_revenue * 0.2  # 広告費を収益の20%と仮定
        roi = ((current_revenue - ad_spend) / ad_spend * 100) if ad_spend > 0 else 0
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">ROI</div>
            <div class="kpi-value">{roi:.1f}%</div>
            <div class="kpi-change kpi-up">
                ROAS: {(current_revenue/ad_spend):.2f}x
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="performance-indicator">
            <span>広告費用</span>
            <div class="indicator-bar">
                <div class="indicator-progress" style="width: 20%;"></div>
            </div>
            <span>¥{ad_spend:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)

# エンゲージメントタブ
with chart_tabs[3]:
    # マルチメトリクスチャート
    fig_engagement = go.Figure()
    
    # エンゲージメント率
    engagement_rate = (current_data['social_engagement'] / current_data['traffic'] * 100).fillna(0)
    
    fig_engagement.add_trace(go.Scatter(
        x=current_data['date'],
        y=engagement_rate,
        mode='lines+markers',
        name='エンゲージメント率 (%)',
        line=dict(color='#3b82f6', width=2)
    ))
    
    # メール開封率
    fig_engagement.add_trace(go.Scatter(
        x=current_data['date'],
        y=current_data['email_open_rate'],
        mode='lines+markers',
        name='メール開封率 (%)',
        line=dict(color='#10b981', width=2)
    ))
    
    # CTR
    fig_engagement.add_trace(go.Scatter(
        x=current_data['date'],
        y=current_data['ctr'],
        mode='lines+markers',
        name='CTR (%)',
        line=dict(color='#f59e0b', width=2)
    ))
    
    fig_engagement.update_layout(
        title="エンゲージメント指標",
        xaxis_title="日付",
        yaxis_title="率 (%)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified',
        legend=dict(
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(59, 130, 246, 0.3)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_engagement, use_container_width=True)
    
    # ソーシャルメディア別エンゲージメント
    st.markdown("#### プラットフォーム別エンゲージメント")
    
    social_cols = st.columns(4)
    platforms = [
        {"name": "Twitter", "icon": "🐦", "engagement": 2834, "growth": 12.5},
        {"name": "LinkedIn", "icon": "💼", "engagement": 1923, "growth": 8.3},
        {"name": "Facebook", "icon": "📘", "engagement": 1456, "growth": -3.2},
        {"name": "Instagram", "icon": "📷", "engagement": 3201, "growth": 25.7}
    ]
    
    for col, platform in zip(social_cols, platforms):
        with col:
            growth_class = "up" if platform['growth'] > 0 else "down"
            st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 2rem;">{platform['icon']}</div>
                <div class="kpi-label">{platform['name']}</div>
                <div class="kpi-value" style="font-size: 1.5rem;">{platform['engagement']:,}</div>
                <div class="kpi-change kpi-{growth_class}">
                    {platform['growth']:+.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

# 詳細メトリクスタブ
with chart_tabs[4]:
    st.markdown("#### ウェブサイトパフォーマンス")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 直帰率
        fig_bounce = go.Figure()
        
        fig_bounce.add_trace(go.Scatter(
            x=current_data['date'],
            y=current_data['bounce_rate'],
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.1)',
            line=dict(color='#ef4444', width=2)
        ))
        
        fig_bounce.update_layout(
            title="直帰率の推移",
            xaxis_title="日付",
            yaxis_title="直帰率 (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_bounce, use_container_width=True)
    
    with col2:
        # 平均セッション時間
        fig_session = go.Figure()
        
        fig_session.add_trace(go.Scatter(
            x=current_data['date'],
            y=current_data['avg_session_duration'],
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)',
            line=dict(color='#10b981', width=2)
        ))
        
        fig_session.update_layout(
            title="平均セッション時間",
            xaxis_title="日付",
            yaxis_title="時間 (秒)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_session, use_container_width=True)
    
    # パフォーマンススコアカード
    st.markdown("#### 総合パフォーマンススコア")
    
    # スコア計算（仮想的な重み付け）
    traffic_score = min(100, (current_traffic / 50000) * 100)
    conversion_score = min(100, conversion_rate * 20)
    revenue_score = min(100, (current_revenue / 1000000) * 100)
    # engagement_rateがSeriesの場合は最新値を取得
    if isinstance(engagement_rate, pd.Series):
        engagement_rate_value = engagement_rate.iloc[-1] if not engagement_rate.empty else 0
    else:
        engagement_rate_value = engagement_rate
    engagement_score = min(100, engagement_rate_value)
    
    overall_score = (traffic_score + conversion_score * 2 + revenue_score * 2 + engagement_score) / 6
    
    score_cols = st.columns(5)
    
    scores = [
        {"label": "総合スコア", "value": overall_score, "weight": "100%"},
        {"label": "トラフィック", "value": traffic_score, "weight": "16.7%"},
        {"label": "コンバージョン", "value": conversion_score, "weight": "33.3%"},
        {"label": "収益", "value": revenue_score, "weight": "33.3%"},
        {"label": "エンゲージメント", "value": engagement_score, "weight": "16.7%"}
    ]
    
    for col, score in zip(score_cols, scores):
        with col:
            color = "#10b981" if score['value'] >= 70 else "#f59e0b" if score['value'] >= 40 else "#ef4444"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{score['label']}</div>
                <div class="kpi-value" style="color: {color};">{score['value']:.1f}</div>
                <div style="font-size: 0.8rem; color: #94a3b8;">重み: {score['weight']}</div>
            </div>
            """, unsafe_allow_html=True)

# アラートセクション
st.markdown("### 🚨 アラート & インサイト")

alert_cols = st.columns(2)

with alert_cols[0]:
    st.markdown("#### ⚠️ 要注意項目")
    
    # 直帰率が高い場合
    avg_bounce = current_data['bounce_rate'].mean()
    if avg_bounce > 40:
        st.markdown(f"""
        <div class="alert-box">
            <strong>高い直帰率</strong><br>
            平均直帰率が{avg_bounce:.1f}%と高めです。<br>
            ランディングページの改善を検討してください。
        </div>
        """, unsafe_allow_html=True)
    
    # コンバージョン率が低い場合
    if conversion_rate < 2:
        st.markdown(f"""
        <div class="alert-box">
            <strong>低コンバージョン率</strong><br>
            CVRが{conversion_rate:.2f}%と目標を下回っています。<br>
            CTAの最適化が必要かもしれません。
        </div>
        """, unsafe_allow_html=True)

with alert_cols[1]:
    st.markdown("#### ✅ 好調な指標")
    
    # エンゲージメントが高い場合
    engagement_check = engagement_rate_value if 'engagement_rate_value' in locals() else (engagement_rate.iloc[-1] if isinstance(engagement_rate, pd.Series) and not engagement_rate.empty else 0)
    if engagement_check > 15:
        st.markdown(f"""
        <div class="alert-box success-box">
            <strong>高エンゲージメント</strong><br>
            エンゲージメント率が{engagement_check:.1f}%と好調です。<br>
            この勢いを維持しましょう。
        </div>
        """, unsafe_allow_html=True)
    
    # 収益が増加している場合
    revenue_growth = calculate_kpi_change(
        current_data['revenue'].iloc[-1],
        current_data['revenue'].iloc[0]
    )
    if revenue_growth['status'] == 'up':
        st.markdown(f"""
        <div class="alert-box success-box">
            <strong>収益成長</strong><br>
            期間中の収益が{revenue_growth['value']:.1f}%増加しました。<br>
            成功要因を分析して横展開しましょう。
        </div>
        """, unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("📈 パフォーマンス設定")
    
    # KPI目標設定
    st.subheader("🎯 KPI目標")
    
    target_traffic = st.number_input("月間トラフィック目標", value=100000, step=10000)
    target_cvr = st.slider("目標CVR (%)", 0.0, 10.0, 3.0, 0.1)
    target_revenue = st.number_input("月間収益目標 (¥)", value=5000000, step=100000)
    
    # 目標達成率
    if st.session_state.time_range == "30d":
        traffic_achievement = (current_traffic / target_traffic * 100) if target_traffic > 0 else 0
        revenue_achievement = (current_revenue / target_revenue * 100) if target_revenue > 0 else 0
        
        st.markdown("### 📊 目標達成率")
        
        st.markdown(f"""
        <div class="performance-indicator">
            <span>トラフィック</span>
            <div class="indicator-bar">
                <div class="indicator-progress" style="width: {min(100, traffic_achievement)}%;"></div>
            </div>
            <span>{traffic_achievement:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="performance-indicator">
            <span>収益</span>
            <div class="indicator-bar">
                <div class="indicator-progress" style="width: {min(100, revenue_achievement)}%;"></div>
            </div>
            <span>{revenue_achievement:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # レポート設定
    st.subheader("📄 レポート設定")
    
    report_frequency = st.selectbox(
        "レポート頻度",
        ["日次", "週次", "月次"]
    )
    
    email_notification = st.checkbox("メール通知を有効化", value=True)
    
    if st.button("📊 レポートを生成", type="primary", use_container_width=True):
        st.success("レポートを生成中...")
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("📊 プロジェクト管理室", use_container_width=True):
        st.switch_page("pages/project_management.py")
    
    if st.button("📦 プロダクト管理", use_container_width=True):
        st.switch_page("pages/product_management.py")

# フッター
st.markdown("---")
st.caption("💡 ヒント: 定期的にKPIをチェックし、トレンドを把握することで、効果的なマーケティング戦略の改善が可能です。アラートを活用して問題を早期に発見しましょう。")