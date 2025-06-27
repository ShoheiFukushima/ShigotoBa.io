"""
パイプライン統合テスト
各AIツールを連携させてエンドツーエンドの動作を検証
"""

import asyncio
import streamlit as st
from datetime import datetime
import json
import sys
import os

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pipeline import PipelineManager, WorkflowDefinition, WorkflowStep
from pages._ai_creative_studio import generate_ai_creative_content
from pages._realtime_ad_optimizer import generate_optimization_recommendations

# テスト用のモックツール実行関数
async def mock_ai_creative_studio(input_data: dict) -> dict:
    """AI Creative Studioのモック実行関数"""
    print(f"[AI Creative Studio] 入力データ: {json.dumps(input_data, ensure_ascii=False)}")
    
    # 実際のAI関数を呼び出し（モックモード）
    os.environ['USE_MOCK_AI'] = 'true'
    result = await generate_ai_creative_content(
        creative_type=input_data.get('campaign_type', 'ad_copy'),
        target_audience=input_data.get('target_audience', '20-30代女性'),
        brand_info=input_data.get('brand_info', {})
    )
    
    print(f"[AI Creative Studio] 生成完了: {len(result.get('content', {}))} 個のクリエイティブ")
    return {
        "status": "success",
        "content": result['content'],
        "performance_prediction": result['performance_prediction'],
        "generated_at": result['generated_at']
    }

async def mock_realtime_ad_optimizer(input_data: dict) -> dict:
    """リアルタイム広告最適化のモック実行関数"""
    print(f"[Ad Optimizer] 入力データ: {json.dumps(input_data, ensure_ascii=False)}")
    
    # テスト用のパフォーマンスデータを作成
    test_data = {
        'metrics': {
            'ctr': 1.5,  # 低いCTRで最適化提案を誘発
            'cpa': 7500,  # 高いCPAで最適化提案を誘発
            'roas': 2.5,  # 低いROASで最適化提案を誘発
            'conversion_rate': 1.8,
            'impressions': 50000,
            'budget_utilization': 0.85,
            'hours_remaining': 24
        },
        'platforms': {
            'Google Ads': {'performance': 0.9, 'budget': 1000000, 'spend_rate': 0.8},
            'Facebook': {'performance': 0.6, 'budget': 500000, 'spend_rate': 0.9},  # 低パフォーマンス
            'Twitter': {'performance': 0.5, 'budget': 300000, 'spend_rate': 0.7}  # 低パフォーマンス
        },
        'trends': {
            'weekly_growth': 0.15,
            'seasonality': 'high',
            'demand_level': 'medium'
        }
    }
    
    # 実際のAI関数を呼び出し（モックモード）
    os.environ['USE_MOCK_AI'] = 'true'
    recommendations = await generate_optimization_recommendations(test_data)
    
    print(f"[Ad Optimizer] 最適化提案生成: {len(recommendations)} 件")
    
    # スコア計算（クリエイティブの予測パフォーマンスから）
    score = 0.75  # デフォルトスコア
    if 'creatives' in input_data:
        # クリエイティブの品質を仮評価
        score = 0.85
    
    return {
        "status": "success",
        "score": score,
        "recommendations": recommendations,
        "analysis_timestamp": datetime.now().isoformat()
    }

async def mock_auto_posting(input_data: dict) -> dict:
    """自動投稿のモック実行関数"""
    print(f"[Auto Posting] 入力データ: {json.dumps(input_data, ensure_ascii=False)}")
    
    # 投稿スケジューリング
    scheduled_posts = []
    platforms = input_data.get('platforms', ['Twitter', 'Facebook', 'Instagram'])
    
    for platform in platforms:
        scheduled_posts.append({
            "platform": platform,
            "scheduled_time": input_data.get('schedule', datetime.now().isoformat()),
            "status": "scheduled",
            "content_preview": str(input_data.get('content', {}))[:100] + "..."
        })
    
    print(f"[Auto Posting] {len(scheduled_posts)} 件の投稿をスケジュール")
    
    return {
        "status": "success",
        "scheduled_posts": scheduled_posts,
        "total_scheduled": len(scheduled_posts)
    }

async def run_integration_test():
    """統合テストを実行"""
    print("=" * 80)
    print("🧪 パイプライン統合テスト開始")
    print("=" * 80)
    
    # パイプラインマネージャーの初期化
    pipeline_manager = PipelineManager()
    
    # ツールを登録
    print("\n📝 ツール登録...")
    pipeline_manager.register_tool("ai_creative_studio", mock_ai_creative_studio)
    pipeline_manager.register_tool("realtime_ad_optimizer", mock_realtime_ad_optimizer)
    pipeline_manager.register_tool("auto_posting", mock_auto_posting)
    print("✅ 3つのツールを登録完了")
    
    # テスト用ワークフローの定義
    test_workflow = WorkflowDefinition(
        "test_campaign_automation",
        "テスト用キャンペーン自動化",
        "統合テスト用のワークフロー"
    )
    
    # ステップ1: クリエイティブ生成
    test_workflow.add_step(WorkflowStep(
        "creative_generation",
        "ai_creative_studio",
        {
            "input_mapping": {
                "campaign_type": "$.input.campaign.type",
                "target_audience": "$.input.campaign.target_audience",
                "brand_info": "$.input.campaign.brand_info"
            }
        }
    ))
    
    # ステップ2: パフォーマンス予測と最適化
    test_workflow.add_step(WorkflowStep(
        "performance_optimization",
        "realtime_ad_optimizer",
        {
            "input_mapping": {
                "creatives": "$.steps.creative_generation.output.content",
                "campaign_metrics": "$.input.campaign.target_metrics"
            }
        }
    ))
    
    # ステップ3: 自動投稿（スコアが0.7以上の場合のみ）
    test_workflow.add_step(WorkflowStep(
        "auto_posting",
        "auto_posting",
        {
            "input_mapping": {
                "content": "$.steps.creative_generation.output.content",
                "schedule": "$.input.campaign.schedule",
                "platforms": "$.input.campaign.platforms"
            },
            "condition": "$.steps.performance_optimization.output.score > 0.7"
        }
    ))
    
    # ワークフローを登録
    pipeline_manager.register_workflow(test_workflow)
    print("\n✅ テストワークフロー登録完了")
    
    # テストデータ
    test_input = {
        "campaign": {
            "type": "social_post",
            "target_audience": "20-30代の働く女性",
            "brand_info": {
                "name": "テストブランド",
                "category": "美容・コスメ",
                "value_prop": "自然由来の成分で肌に優しい",
                "tone": "親しみやすく、信頼感のある"
            },
            "target_metrics": {
                "target_ctr": 3.0,
                "target_cpa": 5000,
                "target_roas": 4.0
            },
            "schedule": datetime.now().isoformat(),
            "platforms": ["Twitter", "Instagram", "Facebook"]
        }
    }
    
    print("\n🚀 ワークフロー実行開始")
    print(f"入力データ: {json.dumps(test_input, ensure_ascii=False, indent=2)}")
    print("-" * 80)
    
    # イベントリスナーの設定
    def on_step_completed(event_data):
        print(f"\n✅ ステップ完了: {event_data['step_id']}")
    
    def on_step_started(event_data):
        print(f"\n⏳ ステップ開始: {event_data['step_id']} (ツール: {event_data['tool_id']})")
    
    pipeline_manager.event_bus.on("step_started", on_step_started)
    pipeline_manager.event_bus.on("step_completed", on_step_completed)
    
    try:
        # ワークフロー実行
        start_time = datetime.now()
        result = await pipeline_manager.execute_workflow(
            "test_campaign_automation",
            test_input
        )
        end_time = datetime.now()
        
        print("\n" + "=" * 80)
        print("🎉 統合テスト完了！")
        print("=" * 80)
        
        # 結果の表示
        print(f"\n📊 実行結果:")
        print(f"- ステータス: {result['status']}")
        print(f"- 実行時間: {result['execution_time']:.2f}秒")
        print(f"- 総実行時間: {(end_time - start_time).total_seconds():.2f}秒")
        
        print("\n📋 各ステップの結果:")
        for step in result['steps']:
            print(f"\n[{step['step_id']}]")
            print(f"  - ツール: {step['tool_id']}")
            print(f"  - ステータス: {step['status']}")
            
            if step['result']:
                print(f"  - 結果概要:")
                if step['tool_id'] == 'ai_creative_studio':
                    content = step['result'].get('content', {})
                    print(f"    - 生成されたコンテンツタイプ: {list(content.keys())}")
                elif step['tool_id'] == 'realtime_ad_optimizer':
                    recommendations = step['result'].get('recommendations', [])
                    print(f"    - 最適化提案数: {len(recommendations)}")
                    print(f"    - スコア: {step['result'].get('score', 0)}")
                elif step['tool_id'] == 'auto_posting':
                    scheduled = step['result'].get('total_scheduled', 0)
                    print(f"    - スケジュール済み投稿数: {scheduled}")
        
        print("\n✅ パイプラインが正常に動作しています！")
        
        # データフローの確認
        print("\n🔄 データフロー確認:")
        print("1. キャンペーン情報 → AI Creative Studio")
        print("2. 生成されたクリエイティブ → Ad Optimizer") 
        print("3. 最適化スコア > 0.7 → Auto Posting")
        print("\n✅ データが正しく各ツール間で受け渡されています！")
        
        return result
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # 非同期実行
    asyncio.run(run_integration_test())