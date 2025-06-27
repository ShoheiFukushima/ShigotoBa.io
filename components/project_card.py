#!/usr/bin/env python3
"""
プロジェクトカードコンポーネント
プロジェクト情報を統一されたカード形式で表示
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from datetime import datetime
import sys
import os

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles.common import get_project_type_style

def render_project_card(
    project_id: str,
    project_data: Dict[str, Any],
    show_actions: bool = False,
    on_click: Optional[callable] = None
) -> None:
    """
    プロジェクトカードを表示
    
    Args:
        project_id: プロジェクトID
        project_data: プロジェクトデータ
            - name: プロジェクト名
            - type: プロジェクトタイプ (dev/marketing/analysis)
            - status: ステータス
            - progress (optional): 進捗率 (0-100)
            - description (optional): 説明
            - tags (optional): タグリスト
            - deadline (optional): 期限
        show_actions: アクションボタンを表示するか
        on_click: クリック時のコールバック関数
    """
    style = get_project_type_style(project_data.get('type', 'default'))
    icon = style['icon']
    color = style['color']
    
    # 進捗率の計算
    progress = project_data.get('progress', 0)
    if 'flow_stage' in project_data:
        progress = (project_data['flow_stage'] / 7) * 100
    
    # カードHTML
    card_html = f"""
    <div class="project-card" style="border-color: {color}40;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <h3 style="color: {color}; margin: 0; font-size: 1.2rem;">{icon} {project_data['name']}</h3>
            <span class="project-type-badge" style="background-color: {color}20; color: {color};">
                {project_data.get('type', 'general').upper()}
            </span>
        </div>
    """
    
    # 説明文
    if 'description' in project_data:
        card_html += f'<p style="color: #cbd5e1; margin: 0.5rem 0; font-size: 0.9rem;">{project_data["description"]}</p>'
    
    # ステータス
    card_html += f'<p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">📊 ステータス: <span style="color: {color};">{project_data["status"]}</span></p>'
    
    # 期限
    if 'deadline' in project_data:
        deadline = project_data['deadline']
        if isinstance(deadline, str):
            deadline_str = deadline
        else:
            deadline_str = deadline.strftime('%Y/%m/%d')
        card_html += f'<p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.9rem;">📅 期限: {deadline_str}</p>'
    
    # タグ
    if 'tags' in project_data and project_data['tags']:
        tags_html = ' '.join([f'<span class="project-tag">{tag}</span>' for tag in project_data['tags']])
        card_html += f'<div style="margin-top: 0.75rem;">{tags_html}</div>'
    
    # プログレスバー
    if progress > 0:
        card_html += f"""
        <div style="margin-top: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                <span style="color: #94a3b8; font-size: 0.8rem;">進捗</span>
                <span style="color: {color}; font-size: 0.8rem; font-weight: bold;">{progress:.0f}%</span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: {color}; height: 100%; width: {progress}%; transition: width 0.3s ease;"></div>
            </div>
        </div>
        """
    else:
        card_html += f'<div class="project-progress" style="background: linear-gradient(90deg, {color}40 0%, transparent 100%);"></div>'
    
    card_html += '</div>'
    
    # カスタムスタイル
    st.markdown("""
    <style>
        .project-tag {
            background: rgba(148, 163, 184, 0.2);
            color: #94a3b8;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            margin-right: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # カードを表示
    if on_click:
        if st.button(label="", key=f"card_{project_id}", help=f"{project_data['name']}を開く"):
            on_click(project_id, project_data)
        st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.markdown(card_html, unsafe_allow_html=True)
    
    # アクションボタン
    if show_actions:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 編集", key=f"edit_{project_id}", use_container_width=True):
                st.session_state[f'editing_{project_id}'] = True
        with col2:
            if st.button("📊 詳細", key=f"detail_{project_id}", use_container_width=True):
                st.switch_page("pages/_project_detail.py")
        with col3:
            if st.button("🗑️ 削除", key=f"delete_{project_id}", use_container_width=True):
                if st.session_state.get(f'confirm_delete_{project_id}'):
                    del st.session_state.projects[project_id]
                    st.rerun()
                else:
                    st.session_state[f'confirm_delete_{project_id}'] = True
                    st.warning("もう一度クリックで削除")

def render_project_grid(
    projects: Dict[str, Dict[str, Any]],
    columns: int = 3,
    show_actions: bool = False,
    filter_type: Optional[str] = None,
    sort_by: str = "name"
) -> None:
    """
    プロジェクトをグリッド表示
    
    Args:
        projects: プロジェクトデータの辞書
        columns: カラム数
        show_actions: アクションボタンを表示するか
        filter_type: フィルタするプロジェクトタイプ
        sort_by: ソート基準 ("name", "status", "created_at")
    """
    # フィルタリング
    filtered_projects = projects
    if filter_type:
        filtered_projects = {
            pid: data for pid, data in projects.items()
            if data.get('type') == filter_type
        }
    
    # ソート
    sorted_items = sorted(
        filtered_projects.items(),
        key=lambda x: x[1].get(sort_by, x[1]['name'])
    )
    
    # グリッド表示
    cols = st.columns(columns)
    for idx, (project_id, project_data) in enumerate(sorted_items):
        with cols[idx % columns]:
            render_project_card(project_id, project_data, show_actions)

def render_project_list(
    projects: Dict[str, Dict[str, Any]],
    show_actions: bool = True,
    show_filters: bool = True
) -> None:
    """
    プロジェクトをリスト形式で表示（フィルタ付き）
    
    Args:
        projects: プロジェクトデータの辞書
        show_actions: アクションボタンを表示するか
        show_filters: フィルタUIを表示するか
    """
    if show_filters:
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            # タイプフィルタ
            project_types = ['すべて'] + list(set(p.get('type', 'general') for p in projects.values()))
            selected_type = st.selectbox("タイプ", project_types, key="project_type_filter")
        
        with col2:
            # ステータスフィルタ
            statuses = ['すべて'] + list(set(p.get('status', '未設定') for p in projects.values()))
            selected_status = st.selectbox("ステータス", statuses, key="project_status_filter")
        
        with col3:
            # ソート
            sort_options = {'名前順': 'name', '作成日順': 'created_at', 'ステータス順': 'status'}
            selected_sort = st.selectbox("並び順", list(sort_options.keys()), key="project_sort")
        
        st.markdown("---")
    
    # フィルタリング
    filtered_projects = projects
    
    if show_filters:
        if selected_type != 'すべて':
            filtered_projects = {
                pid: data for pid, data in filtered_projects.items()
                if data.get('type') == selected_type
            }
        
        if selected_status != 'すべて':
            filtered_projects = {
                pid: data for pid, data in filtered_projects.items()
                if data.get('status') == selected_status
            }
        
        # ソート
        sort_key = sort_options.get(selected_sort, 'name')
        sorted_items = sorted(
            filtered_projects.items(),
            key=lambda x: x[1].get(sort_key, x[1]['name'])
        )
    else:
        sorted_items = list(filtered_projects.items())
    
    # リスト表示
    for project_id, project_data in sorted_items:
        render_project_card(project_id, project_data, show_actions)
        st.markdown("")  # スペース

def render_project_summary_cards(projects: Dict[str, Dict[str, Any]]) -> None:
    """プロジェクトのサマリーカードを表示"""
    
    # 統計情報を計算
    total_projects = len(projects)
    active_projects = len([p for p in projects.values() if p.get('status') in ['進行中', '開発中', '分析中']])
    completed_projects = len([p for p in projects.values() if p.get('status') == '完了'])
    
    # タイプ別カウント
    dev_count = len([p for p in projects.values() if p.get('type') == 'dev'])
    marketing_count = len([p for p in projects.values() if p.get('type') == 'marketing'])
    analysis_count = len([p for p in projects.values() if p.get('type') == 'analysis'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("総プロジェクト", total_projects)
    
    with col2:
        st.metric("アクティブ", active_projects, f"{active_projects/total_projects*100:.0f}%")
    
    with col3:
        st.metric("完了", completed_projects)
    
    with col4:
        most_common_type = max(['dev', 'marketing', 'analysis'], 
                              key=lambda t: len([p for p in projects.values() if p.get('type') == t]))
        style = get_project_type_style(most_common_type)
        st.metric(f"主要タイプ {style['icon']}", most_common_type.upper())