#!/usr/bin/env python3
"""
簡易エラーチェックスクリプト
Streamlitアプリの基本的なエラーを検出
"""

import os
import sys
import importlib.util
import ast

def check_python_syntax(file_path):
    """Pythonファイルの構文エラーをチェック"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax Error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def check_imports(file_path):
    """インポートエラーをチェック"""
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if line.strip().startswith('from ') or line.strip().startswith('import '):
            # Streamlit特有のインポートはスキップ
            if 'streamlit' in line:
                continue
            # 相対インポートをチェック
            if 'from .' in line or 'from ..' in line:
                errors.append(f"Line {i+1}: Relative import found - {line.strip()}")
    
    return errors

def check_page_references(file_path):
    """ページ参照の整合性をチェック"""
    errors = []
    dashboard_dir = os.path.dirname(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # st.switch_page() の参照をチェック
    import re
    page_refs = re.findall(r'st\.switch_page\(["\']([^"\']+)["\']\)', content)
    
    for page_ref in page_refs:
        page_path = os.path.join(dashboard_dir, page_ref)
        if not os.path.exists(page_path):
            errors.append(f"Referenced page not found: {page_ref}")
    
    return errors

def check_session_state_usage(file_path):
    """セッション状態の使用をチェック"""
    warnings = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        # セッション状態の使用前チェック
        if 'st.session_state.' in line and 'if ' not in lines[max(0, i-3):i]:
            if 'not in st.session_state' not in ''.join(lines[max(0, i-5):i]):
                warnings.append(f"Line {i+1}: Session state used without initialization check")
    
    return warnings

def main():
    """メインチェック処理"""
    dashboard_dir = "dashboard"
    
    print("🔍 ダッシュボードファイルのエラーチェックを開始...\n")
    
    # すべてのPythonファイルをチェック
    files_to_check = [
        "home.py",
        "project_management.py", 
        "project_detail.py",
        "development_room.py",
        "ai_settings.py",
        "realtime_chat.py",
        "product_analysis.py",
        "auto_posting.py",
        "scheduler_control.py"
    ]
    
    total_errors = 0
    total_warnings = 0
    
    for file_name in files_to_check:
        file_path = os.path.join(dashboard_dir, file_name)
        
        if not os.path.exists(file_path):
            print(f"❌ {file_name}: ファイルが見つかりません")
            total_errors += 1
            continue
        
        print(f"📄 {file_name} をチェック中...")
        
        # 構文チェック
        syntax_ok, syntax_error = check_python_syntax(file_path)
        if not syntax_ok:
            print(f"  ❌ 構文エラー: {syntax_error}")
            total_errors += 1
            continue
        
        # インポートチェック
        import_errors = check_imports(file_path)
        for error in import_errors:
            print(f"  ⚠️  インポート警告: {error}")
            total_warnings += 1
        
        # ページ参照チェック
        page_errors = check_page_references(file_path)
        for error in page_errors:
            print(f"  ❌ ページ参照エラー: {error}")
            total_errors += 1
        
        # セッション状態チェック
        session_warnings = check_session_state_usage(file_path)
        for warning in session_warnings:
            print(f"  ⚠️  セッション状態警告: {warning}")
            total_warnings += 1
        
        if not import_errors and not page_errors and not session_warnings:
            print(f"  ✅ エラーなし")
    
    print(f"\n📊 チェック完了:")
    print(f"  - エラー: {total_errors}")
    print(f"  - 警告: {total_warnings}")
    
    # ナビゲーション構造の確認
    print("\n🗺️ ナビゲーション構造:")
    print("  1. 🏠 ダッシュボード (home.py)")
    print("     ├─> 📊 プロジェクト管理室 (project_management.py)")
    print("     ├─> 🏗️ 開発室 (development_room.py)")
    print("     └─> その他の機能ページ")
    print("  2. 📊 プロジェクト管理室")
    print("     └─> 📈 プロジェクト室 (project_detail.py)")
    
    return total_errors == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)