#!/usr/bin/env python3
"""
共通ヘッダーコンポーネント
全ページで統一されたヘッダーを提供
"""

import streamlit as st
from datetime import datetime

def render_header():
    """統一されたヘッダーをレンダリング"""
    
    # プロジェクト名を取得
    current_project_name = "なし"
    if hasattr(st.session_state, 'current_project') and st.session_state.current_project:
        if 'projects' in st.session_state:
            project_data = st.session_state.projects.get(st.session_state.current_project)
            if project_data:
                current_project_name = project_data['name']
    
    # CSSスタイル
    st.markdown("""
    <style>
        /* 固定ヘッダー */
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 34px;
            background-color: #1a1f2e;
            border-bottom: 1px solid rgba(59, 130, 246, 0.2);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 10000;  /* 最上位レイヤー */
            width: 100%;
        }
        
        /* Streamlitのサイドバーのz-indexを調整 */
        section[data-testid="stSidebar"] {
            z-index: 9999;  /* ヘッダーの次のレイヤー */
            top: 34px !important;  /* ヘッダーの高さ分下げる */
            height: calc(100vh - 34px) !important;
            transition: all 0.3s ease;
        }
        
        /* サイドバーが折りたたまれた時 */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            width: 30px !important;
            min-width: 30px !important;
            overflow: hidden;
            transition: width 0.3s ease;
            border-right: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        /* 右端7ピクセルのホバーエリア */
        section[data-testid="stSidebar"][aria-expanded="false"]::after {
            content: "";
            position: absolute;
            right: 0;
            top: 34px;
            width: 7px;
            height: calc(100% - 34px);
            background: transparent;
            cursor: pointer;
            z-index: 10001;
        }
        
        /* ホバー時の視覚的フィードバック */
        section[data-testid="stSidebar"][aria-expanded="false"]::after:hover {
            background: rgba(59, 130, 246, 0.2);
        }
        
        /* ホバー時にサイドバーを展開 */
        section[data-testid="stSidebar"][aria-expanded="false"]:hover {
            width: 300px !important;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
        }
        
        /* サイドバーの内容もヘッダー分下げる */
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 10px;
        }
        
        /* サイドバーのトグルボタンを調整 */
        button[kind="header"] {
            top: 44px !important;  /* ヘッダーの下に配置 */
            z-index: 9998;
        }
        
        /* メインコンテンツエリアの調整 */
        section.main > div {
            padding-top: 34px !important;
        }
        
        /* ヘッダーを常に表示 */
        .stApp > header {
            display: none;  /* Streamlitのデフォルトヘッダーを非表示 */
        }
        
        /* 最小化時は全コンテンツを非表示 */
        section[data-testid="stSidebar"][aria-expanded="false"] > div {
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        /* ホバー時にコンテンツを表示 */
        section[data-testid="stSidebar"][aria-expanded="false"]:hover > div {
            opacity: 1;
        }
        
        .header-title {
            font-size: 11px;
            color: #e2e8f0;
            font-weight: 500;
            letter-spacing: 0.5px;
        }
        
        .header-info {
            font-size: 11px;
            color: #94a3b8;
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        /* メインコンテンツのマージン調整 */
        .main {
            margin-top: 34px;
            position: relative;
            z-index: 1;  /* ベースレイヤー */
        }
        
        /* メインコンテンツエリアもヘッダー分調整 */
        .stMain {
            top: 34px !important;
            position: relative;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ヘッダーHTML
    st.markdown(f"""
    <div class="fixed-header">
        <span class="header-title">SHIGOTOBA.IO - マーケティング自動化プラットフォーム</span>
        <div class="header-info">
            <span>プロジェクト: {current_project_name}</span>
            <span>{datetime.now().strftime('%Y/%m/%d %H:%M')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # メインコンテンツ開始
    st.markdown('<div class="main">', unsafe_allow_html=True)

def close_main_content():
    """メインコンテンツdivを閉じる"""
    st.markdown('</div>', unsafe_allow_html=True)