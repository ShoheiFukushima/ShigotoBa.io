#!/usr/bin/env python3
"""
shigotoba.io - AI-Powered Marketing Automation Platform
メインエントリーポイント
"""

import streamlit as st
import sys
import os

# ダッシュボードのパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'dashboard'))

# ダッシュボードのホームページをインポート
from dashboard.home import *