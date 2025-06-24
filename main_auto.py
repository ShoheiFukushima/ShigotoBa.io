#!/usr/bin/env python3
"""
完全自動化対応メインスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.market_analyzer import MarketAnalyzer
from tools.content_generator import ContentGenerator
from tools.automation_orchestrator import AutomationOrchestrator, AutomationLevel
import json
from datetime import datetime

def run_automated_marketing(product_info, automation_level=AutomationLevel.SEMI_AUTO):
    """完全自動化マーケティングを実行"""
    
    print(f"\n🤖 自動化レベル: {automation_level.value}")
    print("="*60)
    
    # Step 1: 市場分析
    print("\n📊 Step 1: 市場分析")
    print("-"*40)
    analyzer = MarketAnalyzer()
    market_analysis = analyzer.analyze_product(product_info)
    
    # Step 2: コンテンツ生成
    print("\n✍️  Step 2: コンテンツ生成")
    print("-"*40)
    generator = ContentGenerator()
    contents = generator.generate_all_content(product_info, market_analysis)
    
    # Step 3: 自動化キャンペーン作成
    print("\n🚀 Step 3: 自動化キャンペーン作成")
    print("-"*40)
    orchestrator = AutomationOrchestrator()
    
    # マーケット分析をシリアライズ可能な形式に変換
    serializable_analysis = {
        "seasonal_insights": market_analysis.seasonal_insights,
        "growth_roadmap": market_analysis.growth_roadmap
    }
    
    campaign = orchestrator.create_campaign(
        product_info,
        serializable_analysis,
        contents
    )
    
    # Step 4: キャンペーン実行
    print("\n⚡ Step 4: キャンペーン実行")
    print("-"*40)
    
    results = orchestrator.execute_campaign(campaign, automation_level)
    
    # Step 5: 結果サマリー
    print("\n📈 実行結果サマリー")
    print("="*60)
    
    if automation_level == AutomationLevel.MANUAL:
        print("\n✅ コンテンツ生成完了！")
        print("\n生成されたコンテンツは以下の場所に保存されています:")
        print(f"📁 /Users/fukushimashouhei/dev/marketing-automation-tools/outputs/")
        print("\n次のアクション:")
        print("1. 生成されたSNS投稿文をコピーして投稿")
        print("2. プレスリリースを配信サービスに登録")
        print("3. メールキャンペーンを設定")
        
    elif automation_level == AutomationLevel.SEMI_AUTO:
        print(f"\n✅ 承認済みタスク: {len(results['tasks_executed'])}件")
        print(f"⏸️  保留中タスク: {len(results['tasks_pending'])}件")
        
        if results['tasks_executed']:
            print("\n実行済みタスク:")
            for task in results['tasks_executed'][:3]:
                print(f"- {task}")
                
    else:  # FULL_AUTO
        print(f"\n🤖 {len(results['tasks_executed'])}件のタスクをスケジューラーに登録しました")
        print("\n自動実行スケジュール:")
        print("- Twitter: 毎日 9:00, 12:00, 19:00")
        print("- ブログ: 火・木 10:00")
        print("- メール: 月曜 8:00")
        print("\n📊 パフォーマンスモニタリングが有効です")
        print("週次レポートが自動生成されます")
    
    # 季節性インサイト表示
    if hasattr(market_analysis, 'seasonal_insights') and market_analysis.seasonal_insights:
        current_month = datetime.now().month
        print(f"\n🗓️ {current_month}月の戦略ポイント:")
        
        if 'next_3_months' in market_analysis.seasonal_insights:
            current_insights = market_analysis.seasonal_insights['next_3_months'][0]
            print(f"- 消費者行動: {current_insights['consumer_behavior'][0]}")
            if current_insights['recommended_campaigns']:
                print(f"- 推奨キャンペーン: {current_insights['recommended_campaigns'][0]}")
    
    return campaign, results

def main():
    """メイン実行関数"""
    
    print("""
╔══════════════════════════════════════════════════════════╗
║        完全自動化マーケティングシステム v2.0             ║
║        - AI分析                                          ║
║        - コンテンツ自動生成                              ║
║        - マルチプラットフォーム自動投稿                  ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 設定ファイル確認
    config_path = '/Users/fukushimashouhei/dev/marketing-automation-tools/automation_config.json'
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        level_str = config.get('automation_level', '手動（生成のみ）')
        
        # 文字列からEnumに変換
        level_map = {
            "手動（生成のみ）": AutomationLevel.MANUAL,
            "半自動（承認後投稿）": AutomationLevel.SEMI_AUTO,
            "完全自動": AutomationLevel.FULL_AUTO
        }
        
        automation_level = level_map.get(level_str, AutomationLevel.MANUAL)
        
        print(f"\n現在の設定: {level_str}")
        
    else:
        print("\n⚠️  設定ファイルが見つかりません")
        print("先に setup_automation.py を実行してください:")
        print("python3 setup_automation.py")
        
        # デフォルトで手動モード
        automation_level = AutomationLevel.MANUAL
    
    # プロダクト情報入力
    print("\n製品情報を入力してください:")
    print("-"*40)
    
    product_info = {}
    product_info['name'] = input("プロダクト名: ").strip() or "MyProduct"
    product_info['category'] = input("カテゴリ: ").strip() or "生産性向上"
    product_info['target'] = input("ターゲット: ").strip() or "個人・中小企業"
    product_info['price'] = input("価格: ").strip() or "月額980円"
    product_info['unique_value'] = input("独自価値: ").strip() or "AI機能搭載"
    product_info['users'] = int(input("現在のユーザー数（新規は0）: ").strip() or "0")
    
    # 実行確認
    print(f"\n実行内容確認:")
    print(json.dumps(product_info, ensure_ascii=False, indent=2))
    print(f"\n自動化レベル: {automation_level.value}")
    
    confirm = input("\n実行しますか？ (y/n): ").strip().lower()
    if confirm != 'y':
        print("キャンセルしました")
        return
    
    # 自動化マーケティング実行
    try:
        campaign, results = run_automated_marketing(product_info, automation_level)
        
        print("\n🎉 完了しました！")
        
        # 完全自動の場合の追加情報
        if automation_level == AutomationLevel.FULL_AUTO:
            print("\n💡 ヒント:")
            print("- ログ確認: automation_logs/ディレクトリ")
            print("- 停止方法: Ctrl+C または stop_automation.py")
            print("- 設定変更: setup_automation.py を再実行")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  実行を中断しました")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()