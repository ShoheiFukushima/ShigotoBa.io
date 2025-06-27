#!/usr/bin/env python3
"""
パイプライン実行モニター
リアルタイムでワークフローの実行状況を監視
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json
import random
import time

# ページ設定
st.set_page_config(
    page_title="パイプラインモニター - shigotoba.io",
    page_icon="📊",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
.pipeline-visualization {
    background: #0f172a;
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
    border: 1px solid #334155;
}
.node {
    background: #1e293b;
    border: 2px solid #334155;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem;
    text-align: center;
    transition: all 0.3s;
}
.node.active {
    border-color: #3b82f6;
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
    animation: pulse 2s infinite;
}
.node.completed {
    border-color: #10b981;
    background: rgba(16, 185, 129, 0.1);
}
.node.failed {
    border-color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
.metric-card {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid #475569;
}
.log-entry {
    background: #1e293b;
    border-left: 3px solid #22c55e;
    padding: 0.75rem;
    margin: 0.5rem 0;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.875rem;
}
.log-entry.error {
    border-left-color: #ef4444;
}
.log-entry.warning {
    border-left-color: #f59e0b;
}
</style>
""", unsafe_allow_html=True)

# メインコンテンツ
st.title("📊 パイプライン実行モニター")
st.markdown("ワークフローの実行状況をリアルタイムで監視")

# 実行中のパイプライン情報（デモデータ）
active_pipeline = {
    "id": "exec_20250627_001",
    "workflow": "キャンペーン完全自動化",
    "status": "running",
    "progress": 66,
    "start_time": datetime.now() - timedelta(minutes=2),
    "steps": [
        {"name": "AI Creative Studio", "status": "completed", "duration": 45},
        {"name": "広告最適化", "status": "running", "duration": None},
        {"name": "自動投稿", "status": "pending", "duration": None}
    ]
}

# メトリクス行
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #64748b; font-size: 0.875rem; margin: 0;">実行中</h3>
        <p style="color: #22c55e; font-size: 2rem; margin: 0.5rem 0; font-weight: bold;">3</p>
        <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">パイプライン</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #64748b; font-size: 0.875rem; margin: 0;">本日の実行</h3>
        <p style="color: #3b82f6; font-size: 2rem; margin: 0.5rem 0; font-weight: bold;">24</p>
        <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">完了: 21 | 失敗: 3</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #64748b; font-size: 0.875rem; margin: 0;">平均実行時間</h3>
        <p style="color: #f59e0b; font-size: 2rem; margin: 0.5rem 0; font-weight: bold;">2:34</p>
        <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">分:秒</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #64748b; font-size: 0.875rem; margin: 0;">成功率</h3>
        <p style="color: #10b981; font-size: 2rem; margin: 0.5rem 0; font-weight: bold;">87.5%</p>
        <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">過去24時間</p>
    </div>
    """, unsafe_allow_html=True)

# パイプライン可視化
st.markdown("### 🔄 実行中のワークフロー")

col1, col2 = st.columns([3, 1])

with col1:
    # パイプラインの視覚的表現
    st.markdown(f"""
    <div class="pipeline-visualization">
        <h3 style="color: #f1f5f9; margin-bottom: 1.5rem;">
            {active_pipeline['workflow']} (ID: {active_pipeline['id']})
        </h3>
        <div style="display: flex; align-items: center; justify-content: space-around;">
    """, unsafe_allow_html=True)
    
    for idx, step in enumerate(active_pipeline['steps']):
        status_class = step['status']
        icon = "✅" if status_class == "completed" else "⏳" if status_class == "running" else "⏸️"
        
        st.markdown(f"""
        <div class="node {status_class}">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <strong style="color: #f1f5f9;">{step['name']}</strong>
            {f'<br><small style="color: #64748b;">{step["duration"]}秒</small>' if step['duration'] else ''}
        </div>
        """, unsafe_allow_html=True)
        
        if idx < len(active_pipeline['steps']) - 1:
            st.markdown("""
            <div style="font-size: 2rem; color: #22c55e;">→</div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # プログレスバー
    progress = st.progress(active_pipeline['progress'] / 100)
    st.markdown(f"**進捗**: {active_pipeline['progress']}% | **経過時間**: {(datetime.now() - active_pipeline['start_time']).seconds // 60}分{(datetime.now() - active_pipeline['start_time']).seconds % 60}秒")

with col2:
    # ステータス情報
    st.markdown("#### 📊 ステータス")
    
    if active_pipeline['status'] == 'running':
        st.success("🟢 実行中")
    elif active_pipeline['status'] == 'completed':
        st.info("✅ 完了")
    else:
        st.error("❌ エラー")
    
    st.markdown("#### ⏱️ タイミング")
    st.markdown(f"""
    - **開始**: {active_pipeline['start_time'].strftime('%H:%M:%S')}
    - **予想終了**: {(active_pipeline['start_time'] + timedelta(minutes=3, seconds=30)).strftime('%H:%M:%S')}
    """)

# パフォーマンスグラフ
st.markdown("### 📈 パフォーマンストレンド")

col1, col2 = st.columns(2)

with col1:
    # 実行時間の推移
    hours = list(range(24))
    execution_times = [random.uniform(120, 240) for _ in hours]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=execution_times,
        mode='lines+markers',
        name='実行時間',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="実行時間の推移（秒）",
        xaxis_title="時間",
        yaxis_title="実行時間（秒）",
        template="plotly_dark",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # 成功率の推移
    success_rates = [random.uniform(80, 95) for _ in hours]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=success_rates,
        mode='lines+markers',
        name='成功率',
        line=dict(color='#10b981', width=2),
        fill='tozeroy',
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="成功率の推移（%）",
        xaxis_title="時間",
        yaxis_title="成功率（%）",
        template="plotly_dark",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 実行ログ
st.markdown("### 📝 実行ログ")

# ログエントリー（デモ）
log_entries = [
    {"time": "16:32:15", "level": "info", "message": "ワークフロー実行開始: キャンペーン完全自動化"},
    {"time": "16:32:16", "level": "info", "message": "[AI Creative Studio] クリエイティブ生成開始"},
    {"time": "16:32:45", "level": "info", "message": "[AI Creative Studio] 5個のクリエイティブを生成完了"},
    {"time": "16:32:46", "level": "info", "message": "[広告最適化] パフォーマンス分析開始"},
    {"time": "16:33:01", "level": "warning", "message": "[広告最適化] CTRが目標値を下回っています"},
    {"time": "16:33:15", "level": "info", "message": "[広告最適化] 最適化提案を3件生成"},
]

# ログ表示
log_container = st.container()
with log_container:
    for entry in reversed(log_entries[-10:]):  # 最新10件を表示
        level_class = "error" if entry["level"] == "error" else "warning" if entry["level"] == "warning" else ""
        st.markdown(f"""
        <div class="log-entry {level_class}">
            <span style="color: #64748b;">[{entry['time']}]</span> 
            <span style="color: {'#ef4444' if entry['level'] == 'error' else '#f59e0b' if entry['level'] == 'warning' else '#22c55e'};">
                [{entry['level'].upper()}]
            </span> 
            {entry['message']}
        </div>
        """, unsafe_allow_html=True)

# 自動更新設定
col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    auto_refresh = st.checkbox("自動更新", value=True)

with col2:
    refresh_interval = st.selectbox("更新間隔", ["5秒", "10秒", "30秒", "1分"], index=1)

with col3:
    if st.button("🔄 手動更新"):
        st.rerun()

# フッター情報
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b;">
    <small>
        最終更新: {}<br>
        アクティブな実行: 3 | キュー待機: 5 | 本日の総実行: 24
    </small>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)