#!/usr/bin/env python3
"""
フローダッシュボード起動スクリプト
"""

import subprocess
import sys
import os

def main():
    print("🔄 Marketing Flow Dashboard 起動中...")
    
    # Streamlitコマンド
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "dashboard/flow_dashboard.py",
        "--theme.base=dark",
        "--theme.primaryColor=#3b82f6",
        "--theme.backgroundColor=#0e1117",
        "--theme.secondaryBackgroundColor=#1a1f2e"
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 ダッシュボードを終了しました")
    except Exception as e:
        print(f"❌ エラー: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())