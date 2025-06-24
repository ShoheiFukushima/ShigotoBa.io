#!/usr/bin/env python3
"""
ナビゲーション修正スクリプト
すべてのページ参照をpages/ディレクトリ対応に更新
"""

import os
import re

def fix_navigation_in_file(filepath):
    """ファイル内のナビゲーションを修正"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ページ名のリスト
    page_names = [
        'home.py',
        'project_management.py',
        'project_detail.py', 
        'development_room.py',
        'ai_settings.py',
        'realtime_chat.py',
        'product_analysis.py',
        'auto_posting.py',
        'scheduler_control.py',
        'flow_dashboard.py',
        'new_product.py'
    ]
    
    # 置換ルール
    replacements = []
    
    # home.pyへの参照はそのまま（メインファイルなので）
    content = content.replace('st.switch_page("home.py")', 'st.switch_page("home")')
    
    # その他のページへの参照はpages/を追加
    for page in page_names:
        if page != 'home.py':
            # 既にpages/が付いていない場合のみ置換
            old_pattern = f'st.switch_page("{page}")'
            new_pattern = f'st.switch_page("pages/{page}")'
            if 'pages/' not in content:  # pages/が含まれていない場合のみ
                content = content.replace(old_pattern, new_pattern)
    
    # ファイルを更新
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed: {filepath}")

def main():
    # dashboardディレクトリのすべてのPythonファイルを処理
    dashboard_dir = "/Users/fukushimashouhei/dev/marketing-automation-tools/dashboard"
    pages_dir = os.path.join(dashboard_dir, "pages")
    
    # home.pyの修正（既に処理済みの可能性あり）
    home_file = os.path.join(dashboard_dir, "home.py")
    if os.path.exists(home_file):
        fix_navigation_in_file(home_file)
    
    # pagesディレクトリ内のすべてのファイルを修正
    if os.path.exists(pages_dir):
        for filename in os.listdir(pages_dir):
            if filename.endswith('.py'):
                filepath = os.path.join(pages_dir, filename)
                fix_navigation_in_file(filepath)
    
    print("\n✅ ナビゲーション修正完了！")

if __name__ == "__main__":
    main()