#!/usr/bin/env python3
"""
ナビゲーションユーティリティ
アプリケーション間のナビゲーションを統一的に管理
"""

import streamlit as st
from typing import List, Dict, Optional, Callable

def navigate_to(page: str) -> None:
    """
    ページ遷移（セッション状態を使用）
    
    Args:
        page: 遷移先のページ名
    """
    st.session_state.current_page = page
    st.rerun()

def switch_page(page_path: str) -> None:
    """
    Streamlitのページ切り替え
    
    Args:
        page_path: 遷移先のページパス
    """
    st.switch_page(page_path)

def create_nav_buttons(
    nav_items: List[Dict],
    columns: int = 3,
    use_container_width: bool = True,
    button_height: Optional[str] = None
) -> None:
    """
    ナビゲーションボタンをグリッドレイアウトで作成
    
    Args:
        nav_items: ナビゲーション項目のリスト
            各項目は以下のキーを持つ辞書:
            - icon: アイコン文字列
            - title: タイトル
            - key: ユニークキー
            - page (optional): ページパス
            - callback (optional): コールバック関数
            - description (optional): 説明文
        columns: カラム数
        use_container_width: ボタンを幅いっぱいに広げるか
        button_height: ボタンの高さ（CSSスタイル）
    """
    cols = st.columns(columns)
    
    for idx, item in enumerate(nav_items):
        with cols[idx % columns]:
            # ボタンテキストを構築
            button_text = f"{item['icon']}\n\n{item['title']}"
            if 'description' in item:
                button_text += f"\n{item['description']}"
            
            # カスタムスタイルがある場合
            if button_height:
                st.markdown(f"""
                <style>
                    div[data-testid="column"]:nth-of-type({(idx % columns) + 1}) button {{
                        height: {button_height};
                        white-space: pre-line;
                    }}
                </style>
                """, unsafe_allow_html=True)
            
            # ボタンを作成
            if st.button(
                button_text,
                key=f"nav_{item['key']}_{idx}",
                use_container_width=use_container_width
            ):
                if 'page' in item:
                    switch_page(item['page'])
                elif 'callback' in item:
                    item['callback']()

def create_breadcrumb(path: List[Dict[str, str]]) -> None:
    """
    パンくずリストを作成
    
    Args:
        path: パスの各要素を表す辞書のリスト
            各要素は 'name' と 'link'（オプション）を持つ
    """
    breadcrumb_html = '<div class="breadcrumb">'
    
    for i, item in enumerate(path):
        if i > 0:
            breadcrumb_html += ' > '
        
        if 'link' in item and i < len(path) - 1:
            breadcrumb_html += f'<a href="{item["link"]}">{item["name"]}</a>'
        else:
            breadcrumb_html += f'<span class="current">{item["name"]}</span>'
    
    breadcrumb_html += '</div>'
    
    st.markdown("""
    <style>
        .breadcrumb {
            padding: 10px 0;
            color: #94a3b8;
            font-size: 0.9rem;
        }
        .breadcrumb a {
            color: #3b82f6;
            text-decoration: none;
        }
        .breadcrumb a:hover {
            text-decoration: underline;
        }
        .breadcrumb .current {
            color: #e2e8f0;
            font-weight: bold;
        }
    </style>
    """ + breadcrumb_html, unsafe_allow_html=True)

def create_tab_navigation(tabs: List[Dict[str, str]], default_tab: str = None) -> str:
    """
    タブナビゲーションを作成
    
    Args:
        tabs: タブのリスト。各要素は 'name' と 'key' を持つ辞書
        default_tab: デフォルトで選択されるタブのキー
    
    Returns:
        選択されたタブのキー
    """
    tab_names = [tab['name'] for tab in tabs]
    tab_keys = [tab['key'] for tab in tabs]
    
    if default_tab and default_tab in tab_keys:
        default_index = tab_keys.index(default_tab)
    else:
        default_index = 0
    
    selected_tab = st.tabs(tab_names)[default_index]
    return tab_keys[tab_names.index(selected_tab)]

# よく使うナビゲーション項目のプリセット
COMMON_NAV_ITEMS = {
    'development': [
        {'icon': '🏗️', 'title': '開発室', 'page': 'pages/_development_room.py', 'key': 'dev_room'},
        {'icon': '📊', 'title': 'プロジェクト管理', 'page': 'pages/_project_management.py', 'key': 'proj_mgmt'},
        {'icon': '📦', 'title': 'プロダクト管理', 'page': 'pages/_product_management.py', 'key': 'prod_mgmt'},
        {'icon': '🧪', 'title': 'A/Bテスト', 'page': 'pages/_ab_testing.py', 'key': 'ab_test'}
    ],
    'analytics': [
        {'icon': '📈', 'title': 'パフォーマンス', 'page': 'pages/_performance_dashboard.py', 'key': 'performance'},
        {'icon': '🎯', 'title': 'アトリビューション分析', 'page': 'pages/_attribution_analysis.py', 'key': 'attribution'},
        {'icon': '🛤️', 'title': 'カスタマージャーニー', 'page': 'pages/_customer_journey_engine.py', 'key': 'journey'},
        {'icon': '💬', 'title': 'AIチャット', 'page': 'pages/_realtime_chat.py', 'key': 'chat'}
    ],
    'marketing': [
        {'icon': '🎨', 'title': 'AI Creative Studio', 'page': 'pages/_ai_creative_studio.py', 'key': 'creative'},
        {'icon': '⚡', 'title': 'リアルタイム最適化', 'page': 'pages/_realtime_ad_optimizer.py', 'key': 'optimizer'},
        {'icon': '🌐', 'title': 'マルチプラットフォーム', 'page': 'pages/_multi_platform_manager.py', 'key': 'multi_platform'},
        {'icon': '💰', 'title': '価格戦略', 'page': 'pages/_pricing_strategy.py', 'key': 'pricing'}
    ],
    'utilities': [
        {'icon': '📚', 'title': 'マニュアル', 'page': 'pages/_user_manual.py', 'key': 'manual'},
        {'icon': '⚙️', 'title': '設定', 'page': 'pages/_ai_settings.py', 'key': 'settings'}
    ]
}

def get_nav_preset(preset_name: str) -> List[Dict]:
    """
    プリセットのナビゲーション項目を取得
    
    Args:
        preset_name: プリセット名 ('development', 'analytics', 'marketing', 'utilities')
    
    Returns:
        ナビゲーション項目のリスト
    """
    return COMMON_NAV_ITEMS.get(preset_name, [])