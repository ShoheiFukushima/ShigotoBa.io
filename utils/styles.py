#!/usr/bin/env python3
"""
共通スタイル設定
全ページで統一されたデザインを提供
"""

import streamlit as st

def load_common_styles():
    """共通CSSスタイルを読み込み"""
    st.markdown("""
    <style>
        /* グローバルスタイル */
        .stApp {
            background-color: #0e1117;
        }
        
        /* ページヘッダー */
        .page-header {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            border: 1px solid rgba(34, 197, 94, 0.2);
            text-align: center;
        }
        
        .page-title {
            color: #22c55e;
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .page-subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
            margin: 0.5rem 0 0 0;
        }
        
        /* コンテンツカード */
        .content-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 1px solid rgba(34, 197, 94, 0.2);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .content-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(34, 197, 94, 0.15);
            border-color: rgba(34, 197, 94, 0.4);
        }
        
        /* メトリクス */
        .metric-card {
            background: rgba(30, 41, 59, 0.5);
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid rgba(34, 197, 94, 0.2);
            text-align: center;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #22c55e;
            margin: 0;
        }
        
        .metric-label {
            color: #94a3b8;
            font-size: 0.9rem;
            margin: 0.25rem 0 0 0;
        }
        
        /* ステータスバッジ */
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .status-active {
            background-color: rgba(34, 197, 94, 0.2);
            color: #22c55e;
        }
        
        .status-pending {
            background-color: rgba(251, 191, 36, 0.2);
            color: #fbbf24;
        }
        
        .status-completed {
            background-color: rgba(59, 130, 246, 0.2);
            color: #3b82f6;
        }
        
        /* プログレスバー */
        .progress-container {
            background-color: rgba(30, 41, 59, 0.5);
            border-radius: 8px;
            height: 8px;
            overflow: hidden;
            margin: 0.5rem 0;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #22c55e, #16a34a);
            border-radius: 8px;
            transition: width 0.3s ease;
        }
        
        /* タブスタイル */
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(30, 41, 59, 0.3);
            border-radius: 8px;
            padding: 0.25rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 6px;
            color: #94a3b8;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(34, 197, 94, 0.2) !important;
            color: #22c55e !important;
        }
        
        /* ボタン最適化 */
        .stButton > button {
            background: linear-gradient(135deg, #22c55e, #16a34a);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
        }
        
        /* 入力フィールド */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            background-color: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: 8px;
            color: #f1f5f9;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #22c55e;
            box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)

def render_page_header(title: str, subtitle: str, icon: str = ""):
    """ページヘッダーをレンダリング"""
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{icon} {title}</h1>
        <p class="page-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(value: str, label: str, delta: str = None):
    """メトリクスカードをレンダリング"""
    delta_html = ""
    if delta:
        color = "#22c55e" if delta.startswith("+") else "#ef4444"
        delta_html = f'<p style="color: {color}; font-size: 0.8rem; margin: 0;">{delta}</p>'
    
    return f"""
    <div class="metric-card">
        <p class="metric-value">{value}</p>
        <p class="metric-label">{label}</p>
        {delta_html}
    </div>
    """

def render_status_badge(status: str):
    """ステータスバッジをレンダリング"""
    status_map = {
        "進行中": "status-active",
        "未着手": "status-pending", 
        "完了": "status-completed",
        "アクティブ": "status-active",
        "保留": "status-pending"
    }
    
    css_class = status_map.get(status, "status-pending")
    return f'<span class="status-badge {css_class}">{status}</span>'

def render_progress_bar(progress: int, height: str = "8px"):
    """プログレスバーをレンダリング"""
    return f"""
    <div class="progress-container" style="height: {height};">
        <div class="progress-bar" style="width: {progress}%;"></div>
    </div>
    """