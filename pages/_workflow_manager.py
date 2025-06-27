#!/usr/bin/env python3
"""
ワークフロー管理画面
AIツールをつなげて自動化パイプラインを作成・実行
"""

import streamlit as st
import json
import asyncio
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Any
import sys
import os

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pipeline import PipelineManager, WorkflowDefinition, WorkflowStep, get_pipeline_manager
from utils.session_state import init_common_session_state
from components.common_sidebar import render_sidebar, get_default_sidebar_config

# ページ設定
st.set_page_config(
    page_title="ワークフロー管理 - shigotoba.io",
    page_icon="🔄",
    layout="wide"
)

# セッション状態の初期化
init_common_session_state()

# サイドバー
sidebar_config = get_default_sidebar_config()
sidebar_config['quick_actions'] = [
    {'label': '新規ワークフロー', 'icon': '➕', 'key': 'new_workflow'},
    {'label': 'テンプレート', 'icon': '📋', 'key': 'templates'},
    {'label': '実行履歴', 'icon': '📊', 'key': 'history'}
]
render_sidebar(sidebar_config)

# カスタムCSS
st.markdown("""
<style>
.workflow-card {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid #475569;
    transition: all 0.3s ease;
}
.workflow-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    border-color: #22c55e;
}
.step-box {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem;
    position: relative;
}
.step-box.active {
    border-color: #22c55e;
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
}
.connector {
    width: 40px;
    height: 2px;
    background: #22c55e;
    margin: 0 auto;
}
.execution-status {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
}
.status-running {
    background: #3b82f6;
    color: white;
}
.status-completed {
    background: #10b981;
    color: white;
}
.status-failed {
    background: #ef4444;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# メインコンテンツ
st.title("🔄 ワークフロー管理")
st.markdown("AIツールを連携させて、マーケティング業務を自動化")

# タブ
tab1, tab2, tab3, tab4 = st.tabs(["📋 ワークフロー一覧", "➕ 新規作成", "▶️ 実行", "📊 実行履歴"])

# パイプラインマネージャー取得
pipeline_manager = get_pipeline_manager()

# ワークフローテンプレート
WORKFLOW_TEMPLATES = {
    "campaign_automation": {
        "name": "キャンペーン完全自動化",
        "description": "企画から配信まで全自動",
        "icon": "🚀",
        "steps": [
            {"tool": "ai_creative_studio", "name": "クリエイティブ生成"},
            {"tool": "realtime_ad_optimizer", "name": "パフォーマンス最適化"},
            {"tool": "auto_posting", "name": "自動投稿"}
        ]
    },
    "content_optimization": {
        "name": "コンテンツ最適化フロー",
        "description": "既存コンテンツの分析と改善",
        "icon": "✨",
        "steps": [
            {"tool": "content_analyzer", "name": "コンテンツ分析"},
            {"tool": "ai_creative_studio", "name": "改善案生成"},
            {"tool": "ab_testing", "name": "A/Bテスト"}
        ]
    },
    "performance_analysis": {
        "name": "パフォーマンス分析",
        "description": "広告効果の詳細分析",
        "icon": "📈",
        "steps": [
            {"tool": "data_collector", "name": "データ収集"},
            {"tool": "realtime_ad_optimizer", "name": "分析・最適化"},
            {"tool": "report_generator", "name": "レポート生成"}
        ]
    }
}

with tab1:
    st.markdown("### 📋 登録済みワークフロー")
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (wf_id, template) in enumerate(WORKFLOW_TEMPLATES.items()):
        with [col1, col2, col3][idx % 3]:
            st.markdown(f"""
            <div class="workflow-card">
                <h3 style="margin: 0; color: #22c55e;">{template['icon']} {template['name']}</h3>
                <p style="color: #94a3b8; margin: 0.5rem 0;">{template['description']}</p>
                <div style="margin-top: 1rem;">
                    <p style="color: #64748b; font-size: 0.875rem;">ステップ数: {len(template['steps'])}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"詳細を見る", key=f"view_{wf_id}"):
                st.session_state.selected_workflow = wf_id

with tab2:
    st.markdown("### ➕ 新規ワークフロー作成")
    
    # ワークフロー基本情報
    col1, col2 = st.columns([2, 1])
    
    with col1:
        workflow_name = st.text_input("ワークフロー名", placeholder="例: 新商品キャンペーン自動化")
        workflow_desc = st.text_area("説明", placeholder="このワークフローの目的を記入...")
    
    with col2:
        workflow_icon = st.selectbox("アイコン", ["🚀", "✨", "📈", "🎯", "💡", "🔧"])
        workflow_category = st.selectbox("カテゴリ", ["マーケティング", "分析", "開発", "その他"])
    
    # ステップ構築
    st.markdown("### 🔧 ワークフローステップ")
    
    if 'workflow_steps' not in st.session_state:
        st.session_state.workflow_steps = []
    
    # 利用可能なツール
    available_tools = {
        "ai_creative_studio": {"name": "AI Creative Studio", "icon": "🎨"},
        "realtime_ad_optimizer": {"name": "リアルタイム広告最適化", "icon": "⚡"},
        "auto_posting": {"name": "自動投稿", "icon": "🚀"},
        "ab_testing": {"name": "A/Bテスト", "icon": "🧪"},
        "content_analyzer": {"name": "コンテンツ分析", "icon": "📊"},
        "report_generator": {"name": "レポート生成", "icon": "📄"}
    }
    
    # ステップ追加UI
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        selected_tool = st.selectbox(
            "ツールを選択",
            options=list(available_tools.keys()),
            format_func=lambda x: f"{available_tools[x]['icon']} {available_tools[x]['name']}"
        )
    
    with col2:
        step_name = st.text_input("ステップ名", value=available_tools[selected_tool]['name'])
    
    with col3:
        if st.button("➕ 追加", use_container_width=True):
            st.session_state.workflow_steps.append({
                "tool": selected_tool,
                "name": step_name,
                "icon": available_tools[selected_tool]['icon']
            })
    
    # ステップ表示
    if st.session_state.workflow_steps:
        st.markdown("#### 現在のステップ構成")
        
        for idx, step in enumerate(st.session_state.workflow_steps):
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                st.markdown(f"**Step {idx + 1}**")
            
            with col2:
                st.markdown(f"""
                <div class="step-box">
                    <strong>{step['icon']} {step['name']}</strong><br>
                    <small style="color: #64748b;">ツール: {step['tool']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.workflow_steps.pop(idx)
                    st.rerun()
            
            if idx < len(st.session_state.workflow_steps) - 1:
                st.markdown('<div class="connector"></div>', unsafe_allow_html=True)
    
    # 保存ボタン
    if st.button("💾 ワークフローを保存", type="primary", disabled=not workflow_name or not st.session_state.workflow_steps):
        # ワークフロー定義を作成
        new_workflow = WorkflowDefinition(
            workflow_id=f"custom_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=workflow_name,
            description=workflow_desc
        )
        
        # ステップを追加
        for idx, step in enumerate(st.session_state.workflow_steps):
            new_workflow.add_step(WorkflowStep(
                step_id=f"step_{idx+1}",
                tool_id=step['tool'],
                config={"name": step['name']}
            ))
        
        # 登録
        pipeline_manager.register_workflow(new_workflow)
        st.success(f"✅ ワークフロー「{workflow_name}」を保存しました！")
        st.session_state.workflow_steps = []

with tab3:
    st.markdown("### ▶️ ワークフロー実行")
    
    # ワークフロー選択
    workflow_id = st.selectbox(
        "実行するワークフローを選択",
        options=list(WORKFLOW_TEMPLATES.keys()),
        format_func=lambda x: f"{WORKFLOW_TEMPLATES[x]['icon']} {WORKFLOW_TEMPLATES[x]['name']}"
    )
    
    if workflow_id:
        template = WORKFLOW_TEMPLATES[workflow_id]
        
        # ワークフロー詳細表示
        st.markdown(f"""
        <div class="workflow-card">
            <h3>{template['icon']} {template['name']}</h3>
            <p style="color: #94a3b8;">{template['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 実行パラメータ
        st.markdown("#### 実行パラメータ")
        
        if workflow_id == "campaign_automation":
            col1, col2 = st.columns(2)
            
            with col1:
                campaign_type = st.selectbox("キャンペーンタイプ", ["SNS広告", "メールキャンペーン", "動画広告"])
                target_audience = st.text_input("ターゲット層", "20-30代の働く女性")
            
            with col2:
                brand_name = st.text_input("ブランド名", "サンプルブランド")
                platforms = st.multiselect("配信プラットフォーム", ["Twitter", "Instagram", "Facebook"], default=["Twitter"])
        
        # 実行ボタン
        if st.button("🚀 ワークフローを実行", type="primary", use_container_width=True):
            with st.spinner("ワークフローを実行中..."):
                # プログレスバー
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 実行シミュレーション
                steps = template['steps']
                for idx, step in enumerate(steps):
                    status_text.text(f"実行中: {step['name']}...")
                    progress_bar.progress((idx + 1) / len(steps))
                    asyncio.run(asyncio.sleep(1))  # シミュレーション
                
                st.success("✅ ワークフローが正常に完了しました！")
                
                # 結果表示
                st.markdown("#### 実行結果")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("生成されたクリエイティブ", "5個", "✅")
                
                with col2:
                    st.metric("予測パフォーマンス", "CTR 3.5%", "📈")
                
                with col3:
                    st.metric("スケジュール済み投稿", "3件", "🚀")

with tab4:
    st.markdown("### 📊 実行履歴")
    
    # ダミーデータ
    history_data = pd.DataFrame({
        'ワークフロー': ['キャンペーン完全自動化', 'コンテンツ最適化フロー', 'パフォーマンス分析'],
        '実行日時': [datetime.now() - pd.Timedelta(hours=i) for i in range(3)],
        'ステータス': ['completed', 'completed', 'running'],
        '実行時間': ['45秒', '32秒', '実行中...'],
        'ステップ': ['3/3', '3/3', '2/3']
    })
    
    # 履歴表示
    for idx, row in history_data.iterrows():
        status_class = f"status-{row['ステータス']}"
        status_text = {
            'completed': '✅ 完了',
            'running': '⏳ 実行中',
            'failed': '❌ 失敗'
        }.get(row['ステータス'], row['ステータス'])
        
        st.markdown(f"""
        <div class="workflow-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #f1f5f9;">{row['ワークフロー']}</h4>
                    <p style="color: #64748b; margin: 0.25rem 0;">
                        {row['実行日時'].strftime('%Y-%m-%d %H:%M')} | 
                        実行時間: {row['実行時間']} | 
                        ステップ: {row['ステップ']}
                    </p>
                </div>
                <div>
                    <span class="execution-status {status_class}">{status_text}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"詳細", key=f"history_{idx}"):
            st.info("実行ログを表示...")

# フローティングアクションボタン
st.markdown("""
<style>
.fab {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 24px;
    color: white;
    cursor: pointer;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
    z-index: 1000;
}
.fab:hover {
    transform: scale(1.1);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
</style>
<div class="fab" title="新規ワークフロー">➕</div>
""", unsafe_allow_html=True)