#!/usr/bin/env python3
"""
セッション状態管理ユーティリティ
Streamlitアプリケーション全体で使用される共通のセッション状態管理機能
"""

import streamlit as st
from typing import Dict, Any, Callable, Optional
from datetime import datetime

def init_session_state(state_config: Dict[str, Any]) -> None:
    """
    セッション状態を初期化
    
    Args:
        state_config: キーとデフォルト値のディクショナリ
    """
    for key, default_value in state_config.items():
        if key not in st.session_state:
            # 値が関数の場合は実行して結果を設定
            if callable(default_value):
                st.session_state[key] = default_value()
            else:
                st.session_state[key] = default_value

def get_default_projects() -> Dict[str, Dict[str, Any]]:
    """デフォルトプロジェクトデータを返す"""
    return {
        "project_1": {
            "name": "ECサイトリニューアル",
            "type": "dev",
            "status": "進行中",
            "flow_stage": 3,
            "created_at": datetime.now().isoformat()
        },
        "project_2": {
            "name": "新製品キャンペーン",
            "type": "marketing", 
            "status": "企画中",
            "flow_stage": 1,
            "created_at": datetime.now().isoformat()
        },
        "project_3": {
            "name": "ユーザー行動分析",
            "type": "analysis",
            "status": "分析中",
            "flow_stage": 2,
            "created_at": datetime.now().isoformat()
        },
        "project_4": {
            "name": "SaaSプラットフォーム開発",
            "type": "dev",
            "status": "開発中",
            "flow_stage": 4,
            "created_at": datetime.now().isoformat()
        },
        "project_5": {
            "name": "価格戦略最適化",
            "type": "analysis",
            "status": "検証中",
            "flow_stage": 2,
            "created_at": datetime.now().isoformat()
        }
    }

def get_default_todos() -> list:
    """デフォルトTODOリストを返す"""
    return [
        {"id": 1, "text": "週次レポートの作成", "done": False, "priority": "high"},
        {"id": 2, "text": "A/Bテスト結果の分析", "done": False, "priority": "medium"},
        {"id": 3, "text": "新規広告クリエイティブの承認", "done": False, "priority": "high"},
        {"id": 4, "text": "競合分析資料の更新", "done": False, "priority": "low"},
        {"id": 5, "text": "月次KPIダッシュボード確認", "done": False, "priority": "medium"}
    ]

def update_session_value(key: str, value: Any) -> None:
    """セッション状態の値を更新"""
    st.session_state[key] = value

def get_session_value(key: str, default: Any = None) -> Any:
    """セッション状態から値を取得"""
    return st.session_state.get(key, default)

def clear_session_state(keys: Optional[list] = None) -> None:
    """
    セッション状態をクリア
    
    Args:
        keys: クリアするキーのリスト。Noneの場合は全てクリア
    """
    if keys is None:
        # 全てクリア
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    else:
        # 指定されたキーのみクリア
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]

def has_session_value(key: str) -> bool:
    """セッション状態にキーが存在するかチェック"""
    return key in st.session_state

# 共通のセッション状態設定
COMMON_SESSION_CONFIG = {
    'initialized': False,
    'current_project': None,
    'projects': get_default_projects,
    'todos': get_default_todos,
    'current_page': 'home',
    'sidebar_expanded': True,
    'theme': 'dark',
    'notifications': [],
    'user_preferences': {}
}

# Shigotoba.io専用のセッション状態設定
SHIGOTOBA_SESSION_CONFIG = {
    'current_page': 'home',
    'project_data': {},
    'ai_outputs': {},
    'approval_status': {},
    'execution_history': [],
    'current_phase': None,
    'ai_modules_status': {},
    'processing': False
}

def init_common_session_state():
    """共通のセッション状態を初期化"""
    # 初期化フラグをチェックして、既に初期化済みならスキップ
    if st.session_state.get('_initialized', False):
        return
    
    init_session_state(COMMON_SESSION_CONFIG)
    
    # Google Sheetsとの同期を試みる（初回のみ）
    if not st.session_state.get('_sheets_synced', False):
        try:
            from .google_sheets_db import sync_sheets_to_session
            sync_sheets_to_session()
            st.session_state._sheets_synced = True
        except Exception as e:
            # エラーが発生してもアプリは動作するようにする
            pass
    
    # 初期化完了フラグを設定
    st.session_state._initialized = True
    
def init_shigotoba_session_state():
    """Shigotoba.io用のセッション状態を初期化"""
    init_session_state(SHIGOTOBA_SESSION_CONFIG)