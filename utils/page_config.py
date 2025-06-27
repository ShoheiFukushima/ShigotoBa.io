#!/usr/bin/env python3
"""
ページ設定ユーティリティ
Streamlitページの標準的な設定を提供
"""

import streamlit as st
from typing import Optional, Literal
import sys
import os

# パスを追加してインポート可能にする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles.common import get_common_styles

def setup_page(
    title: str,
    icon: str = "🚀",
    layout: Literal["wide", "centered"] = "wide",
    initial_sidebar_state: Literal["expanded", "collapsed", "auto"] = "expanded",
    menu_items: Optional[dict] = None,
    apply_common_styles: bool = True
) -> None:
    """
    標準的なページ設定を適用
    
    Args:
        title: ページタイトル
        icon: ページアイコン
        layout: レイアウト（"wide" または "centered"）
        initial_sidebar_state: サイドバーの初期状態
        menu_items: メニューアイテムのカスタマイズ
        apply_common_styles: 共通CSSを適用するか
    """
    # デフォルトのメニューアイテム
    if menu_items is None:
        menu_items = {
            'Get Help': None,
            'Report a bug': None,
            'About': f"# {title}\n\nマーケティング自動化プラットフォーム"
        }
    
    # ページ設定
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
        menu_items=menu_items
    )
    
    # 共通スタイルを適用
    if apply_common_styles:
        st.markdown(get_common_styles(), unsafe_allow_html=True)

def add_custom_css(css: str) -> None:
    """
    カスタムCSSを追加
    
    Args:
        css: 追加するCSSコード
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def set_page_header(
    title: str,
    subtitle: Optional[str] = None,
    divider: bool = True
) -> None:
    """
    ページヘッダーを設定
    
    Args:
        title: メインタイトル
        subtitle: サブタイトル（オプション）
        divider: 区切り線を表示するか
    """
    st.title(title)
    
    if subtitle:
        st.markdown(f"*{subtitle}*")
    
    if divider:
        st.markdown("---")

def create_page_container(padding: str = "1rem") -> None:
    """
    ページコンテナを作成（パディング付き）
    
    Args:
        padding: パディングサイズ
    """
    st.markdown(f"""
    <style>
        .main .block-container {{
            padding: {padding};
        }}
    </style>
    """, unsafe_allow_html=True)

def setup_dark_mode() -> None:
    """ダークモードの設定を適用"""
    dark_mode_css = """
    <style>
        /* ダークモード追加設定 */
        .stTextInput > div > div > input {
            background-color: #1e2329;
            color: #e2e8f0;
            border-color: #2a3441;
        }
        
        .stSelectbox > div > div > div {
            background-color: #1e2329;
            color: #e2e8f0;
        }
        
        .stTextArea > div > div > textarea {
            background-color: #1e2329;
            color: #e2e8f0;
            border-color: #2a3441;
        }
        
        /* メトリクスのスタイル調整 */
        [data-testid="metric-container"] {
            background-color: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* ボタンのホバー効果 */
        .stButton > button:hover {
            border-color: #3b82f6;
            color: #3b82f6;
        }
    </style>
    """
    st.markdown(dark_mode_css, unsafe_allow_html=True)

def setup_responsive_layout() -> None:
    """レスポンシブレイアウトの設定"""
    responsive_css = """
    <style>
        /* モバイル対応 */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem;
            }
            
            [data-testid="column"] {
                margin-bottom: 1rem;
            }
            
            .widget-card {
                padding: 15px;
            }
        }
        
        /* タブレット対応 */
        @media (min-width: 768px) and (max-width: 1024px) {
            .main .block-container {
                padding: 1rem;
            }
        }
    </style>
    """
    st.markdown(responsive_css, unsafe_allow_html=True)

# プリセット設定
class PagePresets:
    """よく使うページ設定のプリセット"""
    
    @staticmethod
    def dashboard():
        """ダッシュボード用設定"""
        setup_page(
            title="shigotoba.io - マーケティング自動化",
            icon="🏠",
            layout="wide"
        )
        setup_dark_mode()
        setup_responsive_layout()
    
    @staticmethod
    def analytics():
        """分析ページ用設定"""
        setup_page(
            title="分析ダッシュボード",
            icon="📊",
            layout="wide"
        )
        setup_dark_mode()
    
    @staticmethod
    def settings():
        """設定ページ用設定"""
        setup_page(
            title="設定",
            icon="⚙️",
            layout="centered"
        )
        setup_dark_mode()
    
    @staticmethod
    def shigotoba():
        """Shigotoba.io用設定"""
        setup_page(
            title="Shigotoba.io - AI専門家集団",
            icon="🏭",
            layout="wide"
        )
        setup_dark_mode()
        # Shigotoba特有のスタイル追加
        add_custom_css("""
            .ai-module-card {
                background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
                border: 2px solid #4a5568;
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                transition: all 0.3s;
            }
            
            .ai-module-card:hover {
                border-color: #3b82f6;
                transform: translateY(-2px);
            }
        """)