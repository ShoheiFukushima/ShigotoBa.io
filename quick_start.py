#!/usr/bin/env python3
"""
クイックスタート - ダッシュボードを簡単に起動
"""

import os
import subprocess
import sys

# Streamlitの設定を自動化
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

# Streamlitコマンドを構築
cmd = [
    sys.executable,
    '-m',
    'streamlit',
    'run',
    'dashboard/app.py',
    '--server.port=8501',
    '--browser.gatherUsageStats=false',
    '--server.headless=true'
]

print("🚀 Publishing Dashboard を起動しています...")
print("ブラウザで http://localhost:8501 を開いてください")
print("終了するには Ctrl+C を押してください\n")

# 実行
try:
    subprocess.run(cmd)
except KeyboardInterrupt:
    print("\n👋 ダッシュボードを終了しました")