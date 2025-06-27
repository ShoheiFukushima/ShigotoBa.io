#!/usr/bin/env python3
"""
共通サイドバーコンポーネント
アプリケーション全体で使用される統一されたサイドバー
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import sys
import os

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.navigation import navigate_to, switch_page

def render_branding(config: Dict[str, Any]) -> None:
    """
    ブランディングセクションを表示
    
    Args:
        config: ブランディング設定
            - title: メインタイトル
            - subtitle: サブタイトル
            - icon: アイコン
            - show_date: 日付を表示するか
    """
    icon = config.get('icon', '🚀')
    title = config.get('title', 'SHIGOTOBA.IO')
    subtitle = config.get('subtitle', 'マーケティング自動化プラットフォーム')
    show_date = config.get('show_date', True)
    
    branding_html = f"""
    <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid #2a3441; margin-bottom: 1rem;">
        <h2 style="color: #22c55e; margin: 0; font-size: 1.5rem;">{icon} {title}</h2>
        <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-style: italic;">{subtitle}</p>
    """
    
    if show_date:
        date_str = datetime.now().strftime('%Y/%m/%d')
        branding_html += f'<p style="color: #64748b; margin: 0.25rem 0 0 0; font-size: 0.8rem;">📅 {date_str}</p>'
    
    branding_html += '</div>'
    
    st.markdown(branding_html, unsafe_allow_html=True)

def render_navigation(nav_items: List[Dict[str, Any]]) -> None:
    """
    ナビゲーションメニューを表示
    
    Args:
        nav_items: ナビゲーション項目のリスト
            各項目は以下のキーを持つ辞書:
            - icon: アイコン
            - label: ラベル
            - page (optional): ページパス
            - callback (optional): コールバック関数
            - divider_after (optional): この項目の後に区切り線を入れるか
    """
    for item in nav_items:
        if st.button(
            f"{item['icon']} {item['label']}",
            key=f"nav_{item.get('key', item['label'])}",
            use_container_width=True
        ):
            if 'page' in item:
                switch_page(item['page'])
            elif 'callback' in item:
                item['callback']()
        
        if item.get('divider_after', False):
            st.markdown("---")

def render_project_selector(projects: Dict[str, Dict[str, Any]]) -> Optional[str]:
    """
    プロジェクトセレクターを表示
    
    Args:
        projects: プロジェクトデータの辞書
    
    Returns:
        選択されたプロジェクトID
    """
    st.markdown("## 📁 プロジェクト")
    
    # 現在のプロジェクトの初期値を設定
    current_project = st.session_state.get('current_project', None)
    default_index = 0
    
    project_names = ["選択してください"] + [data['name'] for data in projects.values()]
    project_ids = [None] + list(projects.keys())
    
    # 現在のプロジェクトがある場合、そのインデックスを見つける
    if current_project and current_project in projects:
        project_name = projects[current_project]['name']
        if project_name in project_names:
            default_index = project_names.index(project_name)
    
    selected = st.selectbox("現在の作業", project_names, index=default_index, label_visibility="collapsed")
    
    selected_project_id = None
    
    if selected != "選択してください":
        for pid, data in projects.items():
            if data['name'] == selected:
                selected_project_id = pid
                st.session_state.current_project = pid
                
                # プロジェクト情報表示
                project_type = data.get('type', 'general')
                status_color = {
                    '進行中': '#10b981',
                    '開発中': '#3b82f6',
                    '企画中': '#f59e0b',
                    '分析中': '#8b5cf6',
                    '検証中': '#ec4899',
                    '完了': '#64748b'
                }.get(data['status'], '#94a3b8')
                
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.5); padding: 1rem; border-radius: 8px; border-left: 3px solid {status_color};">
                    <div style="font-weight: bold; color: #e2e8f0; margin-bottom: 0.5rem;">📊 {data['name']}</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">
                        タイプ: {project_type.upper()} | ステータス: <span style="color: {status_color};">{data['status']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                break
    else:
        # プロジェクト未選択時の初期設定ウィザード表示
        from components.onboarding import render_project_setup_wizard
        if st.button("🎯 プロジェクトを始める", use_container_width=True, type="primary"):
            st.session_state.show_project_wizard = True
    
    return selected_project_id

def render_statistics(stats: List[Dict[str, Any]]) -> None:
    """
    統計情報を表示
    
    Args:
        stats: 統計情報のリスト
            各項目は以下のキーを持つ辞書:
            - label: ラベル
            - value: 値
            - delta (optional): 変化量
            - color (optional): 色
    """
    st.markdown("### 📈 統計情報")
    
    # 2列で表示
    cols = st.columns(2)
    
    for idx, stat in enumerate(stats):
        with cols[idx % 2]:
            value_color = stat.get('color', '#e2e8f0')
            
            if 'delta' in stat:
                st.metric(
                    label=stat['label'],
                    value=stat['value'],
                    delta=stat['delta']
                )
            else:
                st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <div style="color: #94a3b8; font-size: 0.8rem;">{stat['label']}</div>
                    <div style="color: {value_color}; font-size: 1.2rem; font-weight: bold;">{stat['value']}</div>
                </div>
                """, unsafe_allow_html=True)

def render_quick_actions(actions: List[Dict[str, Any]]) -> None:
    """
    クイックアクションボタンを表示
    
    Args:
        actions: アクション項目のリスト
            各項目は以下のキーを持つ辞書:
            - icon: アイコン
            - label: ラベル
            - type: ボタンタイプ ("primary", "secondary")
            - page (optional): ページパス
            - callback (optional): コールバック関数
    """
    st.markdown("### ⚡ クイックアクション")
    
    for action in actions:
        button_type = action.get('type', 'secondary')
        
        if st.button(
            f"{action['icon']} {action['label']}",
            key=f"quick_{action.get('key', action['label'])}",
            type="primary" if button_type == "primary" else "secondary",
            use_container_width=True
        ):
            if 'page' in action:
                switch_page(action['page'])
            elif 'callback' in action:
                action['callback']()

def render_notifications(notifications: List[Dict[str, Any]]) -> None:
    """
    通知を表示
    
    Args:
        notifications: 通知のリスト
            各項目は以下のキーを持つ辞書:
            - type: 通知タイプ ("info", "success", "warning", "error")
            - message: メッセージ
            - timestamp (optional): タイムスタンプ
    """
    st.markdown("### 🔔 通知")
    
    if not notifications:
        st.markdown("*新しい通知はありません*")
        return
    
    for notif in notifications[:5]:  # 最新5件のみ表示
        icon = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }.get(notif['type'], 'ℹ️')
        
        color = {
            'info': '#3b82f6',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444'
        }.get(notif['type'], '#94a3b8')
        
        timestamp = ""
        if 'timestamp' in notif:
            if isinstance(notif['timestamp'], str):
                timestamp = notif['timestamp']
            else:
                timestamp = notif['timestamp'].strftime('%H:%M')
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 0.75rem; border-radius: 8px; border-left: 3px solid {color}; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <span>{icon} {notif['message']}</span>
                <span style="color: #64748b; font-size: 0.75rem;">{timestamp}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar(config: Dict[str, Any]) -> None:
    """
    統合サイドバーを表示
    
    Args:
        config: サイドバー設定
            - branding: ブランディング設定
            - navigation: ナビゲーション項目
            - project_selector: プロジェクトセレクター設定
            - statistics: 統計情報
            - quick_actions: クイックアクション
            - notifications: 通知
            - custom_sections: カスタムセクション
    """
    with st.sidebar:
        # ブランディング
        if 'branding' in config:
            render_branding(config['branding'])
        
        # ナビゲーション
        if 'navigation' in config:
            st.subheader("メニュー")
            render_navigation(config['navigation'])
            st.markdown("---")
        
        # プロジェクトセレクター
        if 'project_selector' in config and config['project_selector'].get('show', True):
            projects = st.session_state.get('projects', {})
            if projects:
                render_project_selector(projects)
                st.markdown("---")
        
        # クイックアクション
        if 'quick_actions' in config:
            render_quick_actions(config['quick_actions'])
            st.markdown("---")
        
        # 統計情報
        if 'statistics' in config:
            render_statistics(config['statistics'])
            st.markdown("---")
        
        # 通知
        if 'notifications' in config:
            render_notifications(config['notifications'])
            st.markdown("---")
        
        # カスタムセクション
        if 'custom_sections' in config:
            for section in config['custom_sections']:
                if 'title' in section:
                    st.subheader(section['title'])
                if 'content' in section:
                    if callable(section['content']):
                        section['content']()
                    else:
                        st.markdown(section['content'])
                if section.get('divider', True):
                    st.markdown("---")
        
        # フッター
        if config.get('show_footer', True):
            st.caption(f"© 2024 {config.get('branding', {}).get('title', 'Shigotoba.io')}")

# プリセット設定
def get_default_sidebar_config() -> Dict[str, Any]:
    """デフォルトのサイドバー設定を返す"""
    return {
        'branding': {
            'icon': '🚀',
            'title': 'SHIGOTOBA.IO',
            'subtitle': 'マーケティング自動化プラットフォーム',
            'show_date': True
        },
        'navigation': [
            {'icon': '🏠', 'label': 'ホーム', 'page': 'app.py'},
            {'icon': '📋', 'label': '開発室', 'page': 'pages/_development_room.py'},
            {'icon': '📊', 'label': 'プロジェクト管理', 'page': 'pages/_project_management.py'},
            {'icon': '📈', 'label': 'パフォーマンス', 'page': 'pages/_performance_dashboard.py', 'divider_after': True},
            {'icon': '⚙️', 'label': '設定', 'page': 'pages/_ai_settings.py'}
        ],
        'project_selector': {
            'show': True
        },
        'statistics': [
            {'label': 'タスク完了', 'value': '42', 'delta': '+12'},
            {'label': '投稿数', 'value': '28', 'delta': '+7'},
            {'label': 'コンテンツ', 'value': '156', 'delta': '+34'},
            {'label': '効率', 'value': '89%', 'delta': '+5%'}
        ],
        'show_footer': True
    }

def get_shigotoba_sidebar_config() -> Dict[str, Any]:
    """Shigotoba.io用のサイドバー設定を返す"""
    return {
        'branding': {
            'icon': '🏭',
            'title': 'Shigotoba.io',
            'subtitle': 'AI専門家集団',
            'show_date': False
        },
        'navigation': [
            {'icon': '🏠', 'label': 'ホーム', 'callback': lambda: navigate_to('home')},
            {'icon': '📝', 'label': '企画書入力', 'callback': lambda: navigate_to('planning')},
            {'icon': '🤖', 'label': 'AI実行状況', 'callback': lambda: navigate_to('ai_status')},
            {'icon': '✅', 'label': '承認ゲート', 'callback': lambda: navigate_to('approval')},
            {'icon': '📊', 'label': 'レポート', 'callback': lambda: navigate_to('report')}
        ],
        'show_footer': True
    }