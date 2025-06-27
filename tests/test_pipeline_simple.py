"""
シンプルなパイプライン統合テスト
Streamlitのコンテキスト外で実行可能なテスト
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 環境変数設定（モックモード）
os.environ['USE_MOCK_AI'] = 'true'

from utils.pipeline import PipelineManager, WorkflowDefinition, WorkflowStep

# シンプルなモック関数
async def simple_creative_generator(input_data: dict) -> dict:
    """シンプルなクリエイティブ生成"""
    print(f"[Creative] 入力: {json.dumps(input_data, ensure_ascii=False)}")
    
    # シンプルな出力
    output = {
        "status": "success",
        "content": {
            "ad_copy": {
                "headline": f"{input_data.get('target_audience', 'ユーザー')}向けの特別キャンペーン",
                "body": "素晴らしい製品をお届けします。",
                "cta": "今すぐチェック"
            },
            "social_post": {
                "twitter": "新商品発売！ #キャンペーン",
                "instagram": "✨新商品のご紹介✨"
            }
        },
        "performance_prediction": {
            "score": 0.85,
            "ctr": 3.5,
            "engagement": 75
        }
    }
    
    print(f"[Creative] 生成完了: {len(output['content'])} タイプ")
    await asyncio.sleep(0.5)  # 処理時間シミュレーション
    return output

async def simple_optimizer(input_data: dict) -> dict:
    """シンプルな最適化エンジン"""
    print(f"[Optimizer] 入力: クリエイティブ {len(input_data.get('creatives', {}))} 個")
    
    # パフォーマンス分析
    score = 0.8  # 仮のスコア
    
    recommendations = [
        {
            "type": "creative_optimization",
            "priority": "high",
            "title": "CTR改善の余地あり",
            "action": "画像を追加することを推奨"
        },
        {
            "type": "targeting",
            "priority": "medium",
            "title": "ターゲティング最適化",
            "action": "年齢層を絞り込む"
        }
    ]
    
    output = {
        "status": "success",
        "score": score,
        "recommendations": recommendations,
        "analysis": "全体的に良好なパフォーマンスが期待できます"
    }
    
    print(f"[Optimizer] 分析完了: スコア {score}, 推奨事項 {len(recommendations)} 件")
    await asyncio.sleep(0.3)
    return output

async def simple_poster(input_data: dict) -> dict:
    """シンプルな投稿スケジューラー"""
    print(f"[Poster] 入力: コンテンツ {len(input_data.get('content', {}))} 個")
    
    platforms = input_data.get('platforms', ['Twitter', 'Instagram'])
    scheduled = []
    
    for platform in platforms:
        scheduled.append({
            "platform": platform,
            "status": "scheduled",
            "time": datetime.now().isoformat()
        })
    
    output = {
        "status": "success",
        "scheduled_count": len(scheduled),
        "platforms": platforms
    }
    
    print(f"[Poster] スケジュール完了: {len(scheduled)} 件")
    await asyncio.sleep(0.2)
    return output

async def run_simple_test():
    """シンプルな統合テスト実行"""
    print("="*60)
    print("🧪 シンプルパイプライン統合テスト")
    print("="*60)
    
    # パイプラインマネージャー初期化
    pm = PipelineManager()
    
    # ツール登録
    pm.register_tool("creative", simple_creative_generator)
    pm.register_tool("optimizer", simple_optimizer)
    pm.register_tool("poster", simple_poster)
    print("✅ ツール登録完了")
    
    # ワークフロー定義
    workflow = WorkflowDefinition(
        "simple_test",
        "シンプルテスト",
        "基本的なパイプラインテスト"
    )
    
    # ステップ追加
    workflow.add_step(WorkflowStep(
        "step1_creative",
        "creative",
        {
            "input_mapping": {
                "campaign_type": "$.input.type",
                "target_audience": "$.input.audience"
            }
        }
    ))
    
    workflow.add_step(WorkflowStep(
        "step2_optimize",
        "optimizer",
        {
            "input_mapping": {
                "creatives": "$.steps.step1_creative.output.content"
            }
        }
    ))
    
    workflow.add_step(WorkflowStep(
        "step3_post",
        "poster",
        {
            "input_mapping": {
                "content": "$.steps.step1_creative.output.content",
                "platforms": "$.input.platforms"
            },
            "condition": "$.steps.step2_optimize.output.score > 0.7"
        }
    ))
    
    pm.register_workflow(workflow)
    print("✅ ワークフロー登録完了")
    
    # テスト入力
    test_input = {
        "type": "social_post",
        "audience": "20-30代女性",
        "platforms": ["Twitter", "Instagram", "Facebook"]
    }
    
    print(f"\n📝 入力データ:")
    print(json.dumps(test_input, ensure_ascii=False, indent=2))
    
    print("\n🚀 パイプライン実行開始...")
    print("-"*60)
    
    try:
        # 実行
        start = datetime.now()
        result = await pm.execute_workflow("simple_test", test_input)
        end = datetime.now()
        
        print("-"*60)
        print("✅ パイプライン実行完了！")
        print(f"\n📊 結果:")
        print(f"- ステータス: {result['status']}")
        print(f"- 実行時間: {(end-start).total_seconds():.2f}秒")
        print(f"- 実行ステップ数: {len(result['steps'])}")
        
        print("\n📋 各ステップの結果:")
        for step in result['steps']:
            status_icon = "✅" if step['status'] == "completed" else "❌"
            print(f"{status_icon} {step['step_id']}: {step['status']}")
        
        # データフロー確認
        print("\n🔄 データフロー:")
        print("1. 入力 → Creative Generator")
        print("2. クリエイティブ → Optimizer (スコア: 0.8)")
        print("3. スコア > 0.7 → Poster (3プラットフォーム)")
        
        print("\n🎉 統合テスト成功！")
        return True
        
    except Exception as e:
        print(f"\n❌ エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 実行
    success = asyncio.run(run_simple_test())
    exit(0 if success else 1)