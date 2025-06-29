#!/usr/bin/env python3
"""
AIパイプラインスタジオ
プロジェクト概要から自動的に完全な事業計画を生成
"""

import streamlit as st
import asyncio
from datetime import datetime
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any

# AIチェーンパイプラインのインポート
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ai_chain_pipeline import get_ai_chain_pipeline, ChainStatus

# ページ設定
st.set_page_config(
    page_title="AIパイプラインスタジオ",
    page_icon="🏭",
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
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        border: 2px solid #3b82f6;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* パイプラインビジュアライザー */
    .pipeline-container {
        background: rgba(30, 41, 59, 0.5);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .pipeline-stage {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }
    
    .pipeline-stage.active {
        border-color: #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
    }
    
    .pipeline-stage.completed {
        border-color: #10b981;
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
    }
    
    .pipeline-stage.failed {
        border-color: #ef4444;
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
    }
    
    .stage-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .stage-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #e2e8f0;
    }
    
    .stage-status {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .status-icon {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .status-waiting {
        background: #6b7280;
    }
    
    .status-running {
        background: #3b82f6;
        animation: pulse 1.5s infinite;
    }
    
    .status-completed {
        background: #10b981;
    }
    
    .status-failed {
        background: #ef4444;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* プログレスバー */
    .progress-bar {
        background: rgba(59, 130, 246, 0.1);
        height: 8px;
        border-radius: 4px;
        margin: 20px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    /* 結果表示エリア */
    .result-container {
        background: rgba(30, 41, 59, 0.5);
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .result-header {
        font-size: 1.1rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .result-content {
        color: #e2e8f0;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    
    /* 入力エリア */
    .input-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        border: 2px solid #3b82f6;
    }
    
    /* アニメーション */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ステータスカード */
    .status-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .status-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3b82f6;
        margin: 10px 0;
    }
    
    .status-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'pipeline_running' not in st.session_state:
    st.session_state.pipeline_running = False
if 'pipeline_results' not in st.session_state:
    st.session_state.pipeline_results = {}
if 'pipeline_progress' not in st.session_state:
    st.session_state.pipeline_progress = 0
if 'stage_statuses' not in st.session_state:
    st.session_state.stage_statuses = {}

# ヘッダー
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏭 AIパイプラインスタジオ</h1>
    <p style="color: #94a3b8;">プロジェクト概要から完全な事業計画を自動生成</p>
</div>
""", unsafe_allow_html=True)

# メインコンテンツ
col1, col2 = st.columns([1, 2])

with col1:
    # 入力エリア
    st.markdown("""
    <div class="input-container">
        <h3 style="color: white; margin-bottom: 20px;">📝 プロジェクト概要入力</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # プロジェクト概要入力
    project_overview = st.text_area(
        "プロジェクトの概要を入力してください",
        placeholder="""例：
AIを活用したマーケティング自動化SaaSプラットフォーム「MarketingFlow AI」を開発したい。

主な機能：
- SNS投稿の自動生成と最適化
- 広告パフォーマンスのリアルタイム分析
- 顧客セグメンテーションの自動化

ターゲット：
中小企業のマーケティング担当者で、限られたリソースで効果的なマーケティングを実施したい人々。

解決したい課題：
マーケティング業務の複雑化と人手不足により、効果的な施策の立案と実行が困難になっている。""",
        height=300
    )
    
    # テンプレート選択
    st.markdown("### 💡 クイックスタートテンプレート")
    template = st.selectbox(
        "テンプレートを選択",
        ["カスタム入力", "SaaS製品", "モバイルアプリ", "ECサイト", "教育サービス"]
    )
    
    if template == "SaaS製品":
        if st.button("テンプレートを使用"):
            st.session_state.template_text = """B2B向けのプロジェクト管理SaaS「ProjectHub Pro」を開発したい。

主な機能：
- リアルタイムコラボレーション
- AI駆動のタスク優先順位付け
- 自動レポート生成
- 他ツールとの連携（Slack、GitHub等）

ターゲット：
IT企業やスタートアップのプロジェクトマネージャー、チームリーダー

解決したい課題：
複数のツールを使い分ける煩雑さと、プロジェクトの可視化不足による進捗管理の困難さ。"""
    
    # 実行ボタン
    if st.button("🚀 AIパイプライン実行", type="primary", use_container_width=True, disabled=st.session_state.pipeline_running):
        if project_overview or st.session_state.get('template_text'):
            st.session_state.pipeline_running = True
            st.session_state.pipeline_results = {}
            st.session_state.stage_statuses = {}
            st.rerun()
        else:
            st.error("プロジェクト概要を入力してください")
    
    # 統計情報
    if st.session_state.pipeline_results:
        st.markdown("### 📊 実行統計")
        
        total_time = sum(
            result.get('execution_time', 0) 
            for result in st.session_state.pipeline_results.values()
            if isinstance(result, dict) and 'execution_time' in result
        )
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.markdown(f"""
            <div class="status-card">
                <div class="status-label">完了ステージ</div>
                <div class="status-value">{len(st.session_state.pipeline_results)}/6</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f"""
            <div class="status-card">
                <div class="status-label">実行時間</div>
                <div class="status-value">{total_time:.1f}秒</div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    # パイプライン可視化
    st.markdown("""
    <div class="pipeline-container">
        <h3 style="color: white; margin-bottom: 20px;">🔄 実行パイプライン</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # プログレスバー
    progress = st.session_state.pipeline_progress
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # パイプラインステージ表示
    pipeline = get_ai_chain_pipeline()
    
    for stage in pipeline.stages:
        status = st.session_state.stage_statuses.get(stage.id, "waiting")
        status_class = f"pipeline-stage {status}"
        
        st.markdown(f"""
        <div class="{status_class}">
            <div class="stage-header">
                <div class="stage-name">{stage.name}</div>
                <div class="stage-status">
                    <div class="status-icon status-{status}">
                        {"⏳" if status == "waiting" else "🔄" if status == "running" else "✅" if status == "completed" else "❌"}
                    </div>
                </div>
            </div>
            <div style="color: #94a3b8; font-size: 0.9rem;">{stage.description}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 結果表示
        if stage.id in st.session_state.pipeline_results:
            result = st.session_state.pipeline_results[stage.id]
            if isinstance(result, dict) and 'output' in result:
                with st.expander(f"📄 {stage.name}の結果", expanded=False):
                    st.markdown(result['output'])

# AIパイプライン実行
async def run_pipeline(project_text):
    """AIパイプラインを実行"""
    pipeline = get_ai_chain_pipeline()
    
    # リセット
    pipeline.results = []
    
    async for update in pipeline.execute_chain(project_text):
        if update['type'] == 'progress':
            # ステージ開始
            st.session_state.stage_statuses[update['stage_id']] = 'running'
            st.session_state.pipeline_progress = update['progress']
            
        elif update['type'] == 'result':
            # ステージ完了
            st.session_state.stage_statuses[update['stage_id']] = 'completed'
            st.session_state.pipeline_results[update['stage_id']] = {
                'output': update['output'],
                'execution_time': update['execution_time']
            }
            st.session_state.pipeline_progress = (len(st.session_state.pipeline_results) / len(pipeline.stages))
            
        elif update['type'] == 'error':
            # エラー発生
            st.session_state.stage_statuses[update['stage_id']] = 'failed'
            st.error(f"エラー: {update['error']}")
            
        elif update['type'] == 'complete':
            # 完了
            st.session_state.pipeline_running = False
            
            # 最終レポート生成
            if 'go_to_market_strategy' in st.session_state.pipeline_results:
                # 可視化データの準備
                create_visualization_data(update['context'])

def create_visualization_data(context):
    """既存の可視化機能用にデータを整形"""
    # プロジェクトデータの作成
    project_data = {
        'id': f'auto_project_{datetime.now().strftime("%Y%m%d%H%M%S")}',
        'name': 'AIパイプライン生成プロジェクト',
        'type': 'ai_generated',
        'status': '分析完了',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ai_analysis': {
            'market_analysis': context.get('market_analysis', ''),
            'competitor_analysis': context.get('competitor_analysis', ''),
            'target_personas': context.get('target_personas', ''),
            'feature_design': context.get('feature_design', ''),
            'pricing_strategy': context.get('pricing_strategy', ''),
            'go_to_market_strategy': context.get('go_to_market_strategy', '')
        }
    }
    
    # セッションに保存
    if 'projects' not in st.session_state:
        st.session_state.projects = {}
    
    st.session_state.projects[project_data['id']] = project_data
    st.session_state.current_ai_project = project_data
    
    # Google Sheetsに保存を試みる
    try:
        from utils.google_sheets_db import sync_session_to_sheets
        sync_session_to_sheets()
    except Exception as e:
        st.warning(f"データの保存に失敗しました: {str(e)}")

# パイプライン実行管理
if st.session_state.pipeline_running and project_overview:
    # 非同期実行
    asyncio.run(run_pipeline(project_overview))
    st.rerun()

# サイドバー
with st.sidebar:
    st.header("🏭 AIパイプラインスタジオ")
    
    st.markdown("""
    ### 💡 使い方
    
    1. **プロジェクト概要を入力**
       - 製品・サービスの概要
       - 主な機能
       - ターゲット顧客
       - 解決したい課題
    
    2. **AIが自動分析**
       - 市場分析
       - 競合分析
       - ペルソナ生成
       - 機能設計
       - 価格戦略
       - GTM戦略
    
    3. **結果を活用**
       - 各分析結果を確認
       - 事業計画書として活用
       - 既存ツールで可視化
    """)
    
    st.markdown("---")
    
    st.header("📊 分析ステージ")
    
    stages_info = [
        ("🏪 市場分析", "市場規模、成長性、トレンド"),
        ("🎯 競合分析", "主要競合と差別化ポイント"),
        ("👥 ペルソナ生成", "詳細なターゲット顧客像"),
        ("🛠️ 機能設計", "MVP機能と技術スタック"),
        ("💰 価格戦略", "最適な価格モデル"),
        ("🚀 GTM戦略", "市場参入戦略")
    ]
    
    for stage_name, stage_desc in stages_info:
        st.markdown(f"""
        **{stage_name}**  
        <small style="color: #94a3b8;">{stage_desc}</small>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # エクスポート機能
    if st.session_state.pipeline_results:
        st.header("📥 エクスポート")
        
        if st.button("📄 レポート生成", use_container_width=True):
            # レポート生成処理
            st.info("レポート生成機能は準備中です")
        
        if st.button("📊 可視化ダッシュボードへ", use_container_width=True):
            st.switch_page("pages/_project_management.py")
    
    st.markdown("---")
    
    if st.button("⬅️ ホームに戻る", type="secondary", use_container_width=True):
        st.switch_page("app.py")