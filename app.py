#!/usr/bin/env python3
"""
shigotoba.io - AI-Powered Marketing Automation Platform
メインエントリーポイント
"""

import streamlit as st
import sys
import os

# パスを追加
current_dir = os.path.dirname(os.path.abspath(__file__))
dashboard_dir = os.path.join(current_dir, 'dashboard')
sys.path.insert(0, current_dir)
sys.path.insert(0, dashboard_dir)

# ページ設定
st.set_page_config(
    page_title="shigotoba.io - マーケティング自動化",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# home.pyの内容を実行
home_path = os.path.join(dashboard_dir, 'home.py')
with open(home_path, 'r', encoding='utf-8') as f:
    code = f.read()
    # __file__を正しいパスに設定
    code = code.replace('__file__', f'"{home_path}"')
    exec(code, {'__file__': home_path})