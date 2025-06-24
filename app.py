#!/usr/bin/env python3
"""
shigotoba.io - AI-Powered Marketing Automation Platform
メインエントリーポイント
"""

import streamlit as st
import subprocess
import sys
import os

# Streamlitアプリを起動
if __name__ == "__main__":
    # dashboard/home.pyを直接実行
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'home.py')
    
    # ファイルの内容を読み込んで実行
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        exec(f.read())