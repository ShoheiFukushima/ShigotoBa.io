#!/usr/bin/env python3
"""
ナビゲーションエラーの最終修正
home.pyへの参照を適切に修正
"""

import os
import re

def fix_navigation_issues():
    """すべてのナビゲーション問題を修正"""
    
    # 1. pages/product_analysis.py の修正
    product_analysis_path = "/Users/fukushimashouhei/dev/marketing-automation-tools/dashboard/pages/product_analysis.py"
    if os.path.exists(product_analysis_path):
        with open(product_analysis_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # homeへの参照を修正（ダッシュボードフォルダのhome.pyを参照）
        content = content.replace('st.switch_page("home")', 'st.switch_page("pages/../home.py")')
        # development_room.pyへの参照を修正
        content = content.replace('st.switch_page("development_room.py")', 'st.switch_page("pages/development_room.py")')
        # flow_dashboard.pyへの参照を修正
        content = content.replace('st.switch_page("flow_dashboard.py")', 'st.switch_page("pages/project_management.py")')
        # realtime_chat.pyへの参照を修正  
        content = content.replace('st.switch_page("realtime_chat.py")', 'st.switch_page("pages/realtime_chat.py")')
        # project_detail.pyへの参照を修正
        content = content.replace('st.switch_page("project_detail.py")', 'st.switch_page("pages/project_detail.py")')
        
        with open(product_analysis_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed: product_analysis.py")
    
    # 2. pages/project_management.py の修正
    project_mgmt_path = "/Users/fukushimashouhei/dev/marketing-automation-tools/dashboard/pages/project_management.py"
    if os.path.exists(project_mgmt_path):
        with open(project_mgmt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # homeへの参照を修正
        content = content.replace('st.switch_page("home")', 'st.switch_page("pages/../home.py")')
        # development_room.pyへの参照を修正
        content = content.replace('st.switch_page("development_room.py")', 'st.switch_page("pages/development_room.py")')
        # product_analysis.pyへの参照を修正
        content = content.replace('st.switch_page("product_analysis.py")', 'st.switch_page("pages/product_analysis.py")')
        # ai_settings.pyへの参照を修正
        content = content.replace('st.switch_page("ai_settings.py")', 'st.switch_page("pages/ai_settings.py")')
        
        with open(project_mgmt_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed: project_management.py")
    
    # 3. pages/project_detail.py の修正
    project_detail_path = "/Users/fukushimashouhei/dev/marketing-automation-tools/dashboard/pages/project_detail.py"
    if os.path.exists(project_detail_path):
        with open(project_detail_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # homeへの参照を修正（パンくずナビゲーションのリンクも含む）
        # JavaScript内のページ参照は変更しない
        content = re.sub(r'st\.switch_page\("home"\)', 'st.switch_page("pages/../home.py")', content)
        # development_room.pyへの参照を修正
        content = content.replace('st.switch_page("development_room.py")', 'st.switch_page("pages/development_room.py")')
        
        with open(project_detail_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed: project_detail.py")
    
    # 4. すべてのpagesファイルを確認して修正
    pages_dir = "/Users/fukushimashouhei/dev/marketing-automation-tools/dashboard/pages"
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(pages_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modified = False
            
            # st.switch_page("home") を修正
            if 'st.switch_page("home")' in content:
                content = content.replace('st.switch_page("home")', 'st.switch_page("pages/../home.py")')
                modified = True
            
            # development_room.py への参照を修正（pages/プレフィックスがない場合）
            if 'st.switch_page("development_room.py")' in content:
                content = content.replace('st.switch_page("development_room.py")', 'st.switch_page("pages/development_room.py")')
                modified = True
            
            # その他のページへの参照も修正（pages/プレフィックスがない場合）
            pages_to_fix = [
                'product_analysis.py', 'project_detail.py', 'ai_settings.py',
                'realtime_chat.py', 'auto_posting.py', 'scheduler_control.py'
            ]
            
            for page in pages_to_fix:
                old_ref = f'st.switch_page("{page}")'
                new_ref = f'st.switch_page("pages/{page}")'
                if old_ref in content:
                    content = content.replace(old_ref, new_ref)
                    modified = True
            
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed navigation in: {filename}")
    
    print("\n✨ ナビゲーション修正完了！")

def main():
    fix_navigation_issues()

if __name__ == "__main__":
    main()