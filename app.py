#!/usr/bin/env python3
"""
shigotoba.io - AI-Powered Marketing Automation Platform
"""

# Streamlitでは直接ファイルをimportする
import sys
import os

# パスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard'))

# home.pyの内容をimport
from dashboard import home