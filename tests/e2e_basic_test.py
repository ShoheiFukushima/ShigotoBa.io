#!/usr/bin/env python3
"""
基本的なE2Eテスト
エラーチェックとナビゲーション確認
"""

import requests
import time

def test_basic_navigation():
    """基本的なナビゲーションテスト"""
    base_url = "http://localhost:8501"
    
    print("🔍 E2Eテスト開始...\n")
    
    # 1. ホームページアクセス
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ ホームページ: アクセス可能")
        else:
            print(f"❌ ホームページ: ステータスコード {response.status_code}")
    except Exception as e:
        print(f"❌ ホームページ: エラー - {e}")
    
    # 2. 各ページの確認
    pages = [
        "pages/project_management.py",
        "pages/development_room.py",
        "pages/ai_settings.py",
        "pages/realtime_chat.py",
        "pages/auto_posting.py",
        "pages/product_analysis.py",
        "pages/scheduler_control.py"
    ]
    
    for page in pages:
        page_name = page.split('/')[-1].replace('.py', '')
        url = f"{base_url}/{page}"
        
        try:
            response = requests.get(url)
            # Streamlitは常に200を返すので、エラーはコンテンツで確認
            if "Error" in response.text or "ModuleNotFoundError" in response.text:
                print(f"❌ {page_name}: エラーが含まれています")
            else:
                print(f"✅ {page_name}: 正常に読み込まれました")
        except Exception as e:
            print(f"❌ {page_name}: アクセスエラー - {e}")
    
    print("\n📊 テスト完了")
    print("ブラウザで http://localhost:8501 にアクセスして動作を確認してください")

if __name__ == "__main__":
    test_basic_navigation()