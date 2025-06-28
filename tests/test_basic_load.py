"""
基本的なページロードテスト
各ページが正常に読み込めるかを確認
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """重要なモジュールがインポートできるか確認"""
    print("🧪 インポートテスト開始...")
    
    try:
        # アプリケーション本体
        import app
        print("✅ app.py - OK")
        
        # パイプライン関連
        from utils.pipeline import PipelineManager
        print("✅ utils/pipeline.py - OK")
        
        # 新規ページ
        from pages import _workflow_manager
        print("✅ pages/_workflow_manager.py - OK")
        
        from pages import _pipeline_monitor
        print("✅ pages/_pipeline_monitor.py - OK")
        
        # AI機能
        from pages._ai_creative_studio import generate_ai_creative_content
        print("✅ AI Creative Studio - OK")
        
        from pages._realtime_ad_optimizer import generate_optimization_recommendations
        print("✅ Realtime Ad Optimizer - OK")
        
        # コンポーネント
        from components.onboarding import render_onboarding_modal
        print("✅ Onboarding - OK")
        
        from components.favorites import init_favorites
        print("✅ Favorites - OK")
        
        from components.search import search_tools
        print("✅ Search - OK")
        
        print("\n🎉 全てのインポートテスト成功！")
        return True
        
    except ImportError as e:
        print(f"\n❌ インポートエラー: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        return False

def test_pipeline_basic():
    """パイプライン基本機能テスト"""
    print("\n🧪 パイプライン基本機能テスト...")
    
    try:
        from utils.pipeline import PipelineManager, WorkflowDefinition, WorkflowStep
        
        # パイプラインマネージャー作成
        pm = PipelineManager()
        print("✅ PipelineManager作成 - OK")
        
        # ワークフロー定義
        wf = WorkflowDefinition("test", "テスト", "テスト用")
        print("✅ WorkflowDefinition作成 - OK")
        
        # ステップ追加
        step = WorkflowStep("step1", "test_tool", {})
        wf.add_step(step)
        print("✅ WorkflowStep追加 - OK")
        
        # ワークフロー登録
        pm.register_workflow(wf)
        print("✅ Workflow登録 - OK")
        
        print("\n🎉 パイプライン基本機能テスト成功！")
        return True
        
    except Exception as e:
        print(f"\n❌ パイプラインテストエラー: {e}")
        return False

def main():
    """メインテスト実行"""
    print("="*60)
    print("📋 Marketing Automation Tools - 基本動作確認テスト")
    print("="*60)
    
    all_passed = True
    
    # インポートテスト
    if not test_imports():
        all_passed = False
    
    # パイプラインテスト
    if not test_pipeline_basic():
        all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ 全てのテストが成功しました！")
        print("🚀 デプロイ準備完了")
    else:
        print("❌ 一部のテストが失敗しました")
        print("🔧 修正が必要です")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())