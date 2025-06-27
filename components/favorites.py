"""
お気に入り・ブックマーク機能コンポーネント
よく使うツールへのクイックアクセスを提供
"""

import streamlit as st
from typing import List, Dict, Optional
import json

def init_favorites():
    """お気に入り機能の初期化"""
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'recent_tools' not in st.session_state:
        st.session_state.recent_tools = []

def add_to_favorites(tool_id: str, tool_name: str, tool_icon: str, tool_path: str):
    """ツールをお気に入りに追加"""
    init_favorites()
    
    favorite = {
        "id": tool_id,
        "name": tool_name,
        "icon": tool_icon,
        "path": tool_path
    }
    
    # 重複チェック
    if not any(f['id'] == tool_id for f in st.session_state.favorites):
        st.session_state.favorites.append(favorite)
        return True
    return False

def remove_from_favorites(tool_id: str):
    """お気に入りから削除"""
    init_favorites()
    st.session_state.favorites = [f for f in st.session_state.favorites if f['id'] != tool_id]

def is_favorite(tool_id: str) -> bool:
    """お気に入りに登録されているかチェック"""
    init_favorites()
    return any(f['id'] == tool_id for f in st.session_state.favorites)

def add_to_recent(tool_id: str, tool_name: str, tool_icon: str, tool_path: str):
    """最近使ったツールに追加"""
    init_favorites()
    
    recent = {
        "id": tool_id,
        "name": tool_name,
        "icon": tool_icon,
        "path": tool_path
    }
    
    # 既存の場合は削除
    st.session_state.recent_tools = [r for r in st.session_state.recent_tools if r['id'] != tool_id]
    
    # 先頭に追加
    st.session_state.recent_tools.insert(0, recent)
    
    # 最大10件まで保持
    st.session_state.recent_tools = st.session_state.recent_tools[:10]

def render_favorites_section():
    """お気に入りセクションの表示"""
    init_favorites()
    
    st.markdown("""
    <style>
    .favorites-container {
        background: #1e293b;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .favorite-item {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s;
    }
    .favorite-item:hover {
        border-color: #22c55e;
        transform: translateX(4px);
    }
    .favorite-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    .favorite-name {
        color: #f1f5f9;
        flex-grow: 1;
    }
    .favorite-remove {
        color: #ef4444;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.3s;
    }
    .favorite-remove:hover {
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="favorites-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### ⭐ お気に入り")
        with col2:
            if st.button("管理", key="manage_favorites"):
                st.session_state.show_favorites_manager = not st.session_state.get('show_favorites_manager', False)
        
        if st.session_state.favorites:
            for favorite in st.session_state.favorites[:5]:  # 最大5件表示
                col1, col2, col3 = st.columns([1, 4, 1])
                
                with col1:
                    st.markdown(f'<span class="favorite-icon">{favorite["icon"]}</span>', unsafe_allow_html=True)
                
                with col2:
                    if st.button(favorite["name"], key=f"fav_{favorite['id']}", use_container_width=True):
                        add_to_recent(favorite["id"], favorite["name"], favorite["icon"], favorite["path"])
                        st.switch_page(favorite["path"])
                
                with col3:
                    if st.button("❌", key=f"remove_{favorite['id']}"):
                        remove_from_favorites(favorite["id"])
                        st.rerun()
        else:
            st.info("⭐ よく使うツールをお気に入りに追加しましょう")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_recent_tools():
    """最近使ったツールの表示"""
    init_favorites()
    
    if st.session_state.recent_tools:
        st.markdown("### 🕒 最近使ったツール")
        
        cols = st.columns(min(len(st.session_state.recent_tools), 5))
        for i, recent in enumerate(st.session_state.recent_tools[:5]):
            with cols[i]:
                if st.button(f"{recent['icon']} {recent['name']}", 
                           key=f"recent_{recent['id']}", 
                           use_container_width=True):
                    add_to_recent(recent["id"], recent["name"], recent["icon"], recent["path"])
                    st.switch_page(recent["path"])

def render_favorite_button(tool_id: str, tool_name: str, tool_icon: str, tool_path: str):
    """各ツールページに表示するお気に入りボタン"""
    init_favorites()
    
    is_fav = is_favorite(tool_id)
    
    col1, col2 = st.columns([5, 1])
    with col2:
        if is_fav:
            if st.button("⭐ お気に入り解除", key=f"unfav_{tool_id}"):
                remove_from_favorites(tool_id)
                st.rerun()
        else:
            if st.button("☆ お気に入りに追加", key=f"fav_{tool_id}", type="secondary"):
                if add_to_favorites(tool_id, tool_name, tool_icon, tool_path):
                    st.success("お気に入りに追加しました！")
                    st.rerun()

def render_favorites_manager():
    """お気に入り管理画面"""
    if st.session_state.get('show_favorites_manager', False):
        st.markdown("### ⭐ お気に入り管理")
        
        if st.session_state.favorites:
            for i, favorite in enumerate(st.session_state.favorites):
                col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
                
                with col1:
                    st.write(favorite["icon"])
                
                with col2:
                    st.write(favorite["name"])
                
                with col3:
                    # 順序変更ボタン
                    if i > 0:
                        if st.button("↑", key=f"up_{favorite['id']}"):
                            st.session_state.favorites[i], st.session_state.favorites[i-1] = \
                                st.session_state.favorites[i-1], st.session_state.favorites[i]
                            st.rerun()
                
                with col4:
                    if st.button("削除", key=f"del_{favorite['id']}"):
                        remove_from_favorites(favorite["id"])
                        st.rerun()
        else:
            st.info("お気に入りはまだありません")
        
        if st.button("閉じる", key="close_manager"):
            st.session_state.show_favorites_manager = False
            st.rerun()

def get_quick_access_tools() -> List[Dict]:
    """クイックアクセス用のツールリスト（お気に入り優先）"""
    init_favorites()
    
    # お気に入りが優先
    tools = st.session_state.favorites[:3]
    
    # お気に入りが3件未満の場合は最近使ったツールで補完
    if len(tools) < 3:
        for recent in st.session_state.recent_tools:
            if not any(t['id'] == recent['id'] for t in tools):
                tools.append(recent)
                if len(tools) >= 3:
                    break
    
    # それでも足りない場合はデフォルトツール
    default_tools = [
        {"id": "dev_room", "name": "開発室", "icon": "🏗️", "path": "pages/_development_room.py"},
        {"id": "project_mgmt", "name": "プロジェクト管理", "icon": "📊", "path": "pages/_project_management.py"},
        {"id": "ai_chat", "name": "AIチャット", "icon": "💬", "path": "pages/_realtime_chat.py"}
    ]
    
    for default in default_tools:
        if len(tools) >= 3:
            break
        if not any(t['id'] == default['id'] for t in tools):
            tools.append(default)
    
    return tools[:3]