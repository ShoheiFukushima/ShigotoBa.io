#!/usr/bin/env python3
"""
プロジェクト管理室
全プロジェクトの一覧・管理・監視機能
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ページ設定
st.set_page_config(
    page_title="プロジェクト管理室",
    page_icon="📊",
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
    
    /* パンくずナビゲーション */
    .breadcrumb {
        background: rgba(30, 41, 59, 0.5);
        padding: 10px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }
    
    .breadcrumb a {
        color: #3b82f6;
        text-decoration: none;
    }
    
    .breadcrumb a:hover {
        text-decoration: underline;
    }
    
    /* プロジェクトカード */
    .project-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
        border-color: #3b82f6;
    }
    
    .project-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .project-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #e2e8f0;
        margin: 0;
    }
    
    .project-status {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .status-planning {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
    }
    
    .status-completed {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
    }
    
    .status-paused {
        background: rgba(107, 114, 128, 0.2);
        color: #6b7280;
    }
    
    .project-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin: 15px 0;
    }
    
    .detail-item {
        text-align: center;
    }
    
    .detail-label {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 5px;
    }
    
    .detail-value {
        font-weight: bold;
        color: #e2e8f0;
    }
    
    /* プロジェクト統計 */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3b82f6;
        margin: 10px 0;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* フィルター・検索 */
    .filter-container {
        background: rgba(30, 41, 59, 0.5);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    /* アクションボタン */
    .action-buttons {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
    
    .btn-primary {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    
    .btn-secondary {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'projects' not in st.session_state:
    st.session_state.projects = {}

# パンくずナビゲーション
st.markdown("""
<div class="breadcrumb">
    <a href="javascript:void(0)" onclick="window.parent.postMessage({type: 'streamlit:rerun', data: {page: 'home.py'}}, '*')">🏠 ダッシュボード</a>
    <span style="color: #94a3b8;"> > </span>
    <span style="color: #e2e8f0;">📊 プロジェクト管理室</span>
</div>
""", unsafe_allow_html=True)

# ヘッダー
st.title("📊 プロジェクト管理室")
st.caption("全プロジェクトの統合管理・監視センター")

# 戻るボタン
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    if st.button("⬅️ ダッシュボードに戻る", type="secondary"):
        st.switch_page("app.py")

with col3:
    if st.button("➕ 新規プロジェクト", type="primary"):
        st.switch_page("pages/development_room.py")

# プロジェクト統計
if st.session_state.projects:
    project_list = list(st.session_state.projects.values())
    
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_projects = len(project_list)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_projects}</div>
            <div class="stat-label">総プロジェクト数</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_projects = len([p for p in project_list if p.get('status', 'active') == 'active'])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{active_projects}</div>
            <div class="stat-label">アクティブ</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_progress = sum(p['flow_stage'] for p in project_list) / len(project_list) if project_list else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_progress:.1f}</div>
            <div class="stat-label">平均進捗ステージ</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        completed_projects = len([p for p in project_list if p['flow_stage'] >= 7])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{completed_projects}</div>
            <div class="stat-label">完了プロジェクト</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        success_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{success_rate:.1f}%</div>
            <div class="stat-label">完了率</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# フィルター・検索
st.markdown("### 🔍 フィルター・検索")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    status_filter = st.selectbox(
        "ステータス",
        ["全て", "アクティブ", "計画中", "一時停止", "完了"],
        key="status_filter"
    )

with filter_col2:
    stage_filter = st.selectbox(
        "進捗ステージ",
        ["全ステージ", "Stage 1-2", "Stage 3-4", "Stage 5-6", "Stage 7-8"],
        key="stage_filter"
    )

with filter_col3:
    search_term = st.text_input("プロジェクト名検索", placeholder="検索キーワード...")

# プロジェクト一覧表示
st.markdown("### 📋 プロジェクト一覧")

if st.session_state.projects:
    # フィルタリング
    filtered_projects = {}
    
    for pid, project in st.session_state.projects.items():
        # ステータスフィルター
        if status_filter != "全て":
            project_status = project.get('status', 'active')
            status_map = {
                "アクティブ": "active",
                "計画中": "planning", 
                "一時停止": "paused",
                "完了": "completed"
            }
            if project_status != status_map.get(status_filter):
                continue
        
        # ステージフィルター
        if stage_filter != "全ステージ":
            stage = project['flow_stage']
            stage_ranges = {
                "Stage 1-2": (0, 1),
                "Stage 3-4": (2, 3),
                "Stage 5-6": (4, 5),
                "Stage 7-8": (6, 7)
            }
            min_stage, max_stage = stage_ranges[stage_filter]
            if not (min_stage <= stage <= max_stage):
                continue
        
        # 検索フィルター
        if search_term and search_term.lower() not in project['name'].lower():
            continue
        
        filtered_projects[pid] = project
    
    if filtered_projects:
        for pid, project in filtered_projects.items():
            st.markdown(f"""
            <div class="project-card">
                <div class="project-header">
                    <h3 class="project-title">{project['name']}</h3>
                    <div class="project-status status-{project.get('status', 'active')}">{project.get('status', 'active').upper()}</div>
                </div>
                <div class="project-details">
                    <div class="detail-item">
                        <div class="detail-label">進捗ステージ</div>
                        <div class="detail-value">Stage {project['flow_stage'] + 1}/8</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">進捗率</div>
                        <div class="detail-value">{(project['flow_stage'] / 7 * 100):.0f}%</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">作成日</div>
                        <div class="detail-value">{project['created_at'][:10]}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">最終更新</div>
                        <div class="detail-value">{datetime.now().strftime('%m/%d')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # プロジェクトアクションボタン
            action_col1, action_col2, action_col3, action_col4 = st.columns(4)
            
            with action_col1:
                if st.button(f"📊 詳細表示", key=f"detail_{pid}"):
                    st.session_state.current_project_id = pid
                    st.switch_page("pages/project_detail.py")
            
            with action_col2:
                if st.button(f"✏️ 編集", key=f"edit_{pid}"):
                    st.session_state.current_project_id = pid
                    st.switch_page("pages/development_room.py")
            
            with action_col3:
                if st.button(f"📈 分析", key=f"analyze_{pid}"):
                    st.session_state.current_project_id = pid
                    st.switch_page("pages/product_analysis.py")
            
            with action_col4:
                if st.button(f"🗑️ 削除", key=f"delete_{pid}"):
                    if st.session_state.get(f"confirm_delete_{pid}", False):
                        del st.session_state.projects[pid]
                        st.success(f"プロジェクト '{project['name']}' を削除しました")
                        st.rerun()
                    else:
                        st.session_state[f"confirm_delete_{pid}"] = True
                        st.warning("もう一度クリックして削除を確認してください")
            
            st.markdown("---")
    
    else:
        st.info("フィルター条件に一致するプロジェクトがありません")

else:
    st.info("まだプロジェクトがありません")
    st.markdown("""
    ### 🚀 最初のプロジェクトを作成しましょう
    
    新規プロジェクトを作成して、マーケティング自動化を始めましょう。
    """)
    
    if st.button("➕ プロジェクト作成", type="primary", use_container_width=True):
        st.switch_page("pages/development_room.py")

# プロジェクト進捗チャート（プロジェクトがある場合）
if st.session_state.projects:
    st.markdown("### 📊 プロジェクト進捗分析")
    
    chart_tab1, chart_tab2 = st.tabs(["ステージ分布", "時系列進捗"])
    
    with chart_tab1:
        # ステージ分布円グラフ
        stage_counts = {}
        stage_names = [
            "プロダクト入力", "調査フェーズ", "ベンチマーク策定", "ベネフィット決定",
            "マーケティング施策", "コンテンツ作成", "デプロイメント", "測定・分析"
        ]
        
        for i in range(8):
            stage_counts[f"Stage {i+1}: {stage_names[i]}"] = len([
                p for p in st.session_state.projects.values() 
                if p['flow_stage'] == i
            ])
        
        if any(stage_counts.values()):
            fig_pie = px.pie(
                values=list(stage_counts.values()),
                names=list(stage_counts.keys()),
                title="プロジェクトのステージ分布",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with chart_tab2:
        # 仮想的な時系列データ（実際の実装では実際のデータを使用）
        dates = pd.date_range(start='2024-01-01', end='2025-01-15', freq='W')
        cumulative_projects = []
        completed_projects = []
        
        for i, date in enumerate(dates):
            cumulative_projects.append(min(i + 1, len(st.session_state.projects)))
            completed_projects.append(len([p for p in st.session_state.projects.values() if p['flow_stage'] >= 7]))
        
        fig_line = go.Figure()
        
        fig_line.add_trace(go.Scatter(
            x=dates,
            y=cumulative_projects,
            mode='lines+markers',
            name='累積プロジェクト数',
            line=dict(color='#3b82f6', width=3)
        ))
        
        fig_line.add_trace(go.Scatter(
            x=dates,
            y=completed_projects,
            mode='lines+markers',
            name='完了プロジェクト数',
            line=dict(color='#10b981', width=3)
        ))
        
        fig_line.update_layout(
            title="プロジェクト進捗の時系列推移",
            xaxis_title="日付",
            yaxis_title="プロジェクト数",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                bgcolor='rgba(30, 41, 59, 0.8)',
                bordercolor='rgba(59, 130, 246, 0.3)',
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig_line, use_container_width=True)

# サイドバー
with st.sidebar:
    st.header("📊 管理室ダッシュボード")
    
    # クイックスタッツ
    if st.session_state.projects:
        st.subheader("📈 クイック統計")
        
        project_list = list(st.session_state.projects.values())
        
        # 今日作成されたプロジェクト
        today_projects = len([
            p for p in project_list 
            if p['created_at'].startswith(datetime.now().strftime('%Y-%m-%d'))
        ])
        st.metric("今日作成", today_projects)
        
        # 平均完了時間（仮想データ）
        st.metric("平均完了時間", "12.3日")
        
        # 成功率
        total = len(project_list)
        completed = len([p for p in project_list if p['flow_stage'] >= 7])
        success_rate = (completed / total * 100) if total > 0 else 0
        st.metric("成功率", f"{success_rate:.1f}%")
    
    st.markdown("---")
    
    # プロジェクトアクション
    st.subheader("⚡ クイックアクション")
    
    if st.button("🚀 新規プロジェクト", type="primary", use_container_width=True):
        st.switch_page("pages/development_room.py")
    
    if st.button("📊 一括分析", use_container_width=True):
        st.info("一括分析機能は開発中です")
    
    if st.button("📥 データエクスポート", use_container_width=True):
        if st.session_state.projects:
            export_data = {
                "export_date": datetime.now().isoformat(),
                "total_projects": len(st.session_state.projects),
                "projects": st.session_state.projects
            }
            
            st.download_button(
                label="💾 JSON ダウンロード",
                data=json.dumps(export_data, ensure_ascii=False, indent=2),
                file_name=f"projects_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.warning("エクスポートするプロジェクトがありません")
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ダッシュボード", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("🏗️ 開発室", use_container_width=True):
        st.switch_page("pages/development_room.py")
    
    if st.button("🤖 AI設定", use_container_width=True):
        st.switch_page("pages/ai_settings.py")

# フッター
st.markdown("---")
st.caption("💡 ヒント: プロジェクトカードをクリックして詳細を確認できます。フィルター機能で効率的にプロジェクトを管理しましょう。")