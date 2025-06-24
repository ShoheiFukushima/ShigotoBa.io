#!/usr/bin/env python3
"""
残りのナビゲーションエラーを修正
"""

import os
import re

def fix_home_references(filepath):
    """homeページへの参照を修正"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # st.switch_page("home") を空文字列に置換（メインページへは直接ナビゲートできない）
    content = content.replace('st.switch_page("home")', 'st.switch_page("__main__")')
    
    # development_room.py への参照を修正
    content = content.replace('st.switch_page("development_room.py")', 'st.switch_page("pages/development_room.py")')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed: {filepath}")

def main():
    pages_dir = "/Users/fukushimashouhei/dev/marketing-automation-tools/dashboard/pages"
    
    # すべてのページファイルを修正
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(pages_dir, filename)
            fix_home_references(filepath)
    
    print("\n✅ 残りのナビゲーション修正完了！")

if __name__ == "__main__":
    main()