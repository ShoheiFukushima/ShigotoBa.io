#!/usr/bin/env python3
"""
マーケティング自動化ツール - メインスクリプト
市場分析とコンテンツ生成を統合実行
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.market_analyzer import MarketAnalyzer
from tools.content_generator import ContentGenerator
import json
from datetime import datetime

def run_full_marketing_automation(product_info):
    """プロダクトの完全なマーケティング自動化を実行"""
    
    print(f"\n🚀 {product_info['name']}のマーケティング自動化を開始します\n")
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
    
    # Step 3: レポート作成
    print("\n📋 Step 3: 統合レポート作成")
    print("-"*40)
    create_marketing_report(product_info, market_analysis, contents)
    
    print("\n✅ マーケティング自動化が完了しました！")
    print("="*60)
    
    return market_analysis, contents

def create_marketing_report(product_info, market_analysis, contents):
    """マーケティングレポートを作成"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f"/Users/fukushimashouhei/dev/marketing-automation-tools/outputs/{product_info['name']}_marketing_report_{timestamp}.md"
    
    report = f"""# {product_info['name']} マーケティングレポート

生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}

## 1. プロダクト概要

- **製品名**: {product_info['name']}
- **カテゴリ**: {product_info['category']}
- **ターゲット**: {product_info.get('target', '未定義')}
- **価格**: {product_info.get('price', '未定義')}

## 2. 市場分析サマリー

{market_analysis.summary if hasattr(market_analysis, 'summary') else '分析結果なし'}

## 3. 推奨マーケティング戦略

### 3.1 優先チャネル

"""
    
    if hasattr(market_analysis, 'recommended_channels'):
        for channel in market_analysis.recommended_channels[:3]:
            report += f"- **{channel['channel']}**: {channel['strategy']}\n"
    
    report += f"""

### 3.2 キーメッセージ

- {product_info.get('unique_value', 'ユニークな価値提案')}
- {product_info.get('benefit1', '主要なベネフィット')}
- {product_info.get('benefit2', '副次的なベネフィット')}

## 4. コンテンツ生成結果

### 4.1 生成されたコンテンツ一覧

- ✅ プロダクト説明文
- ✅ SNS投稿文（Twitter/X, LinkedIn）
- ✅ プレスリリース
- ✅ ランディングページコピー
- ✅ メールキャンペーン

### 4.2 次のアクション

1. **即実行可能**
   - SNS投稿の開始
   - ランディングページの構築
   
2. **1週間以内**
   - プレスリリースの配信
   - メールキャンペーンの設定
   
3. **1ヶ月以内**
   - 効果測定と最適化
   - A/Bテストの実施

## 5. 成功指標（KPI）

- **認知度**: SNSフォロワー数、インプレッション数
- **興味関心**: ウェブサイト訪問数、滞在時間
- **コンバージョン**: 無料トライアル登録数、有料転換率

---

*このレポートは自動生成されました。詳細なデータは個別のJSONファイルをご確認ください。*
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 レポートを保存しました: {report_path}")

def load_product_from_json(json_path):
    """JSONファイルからプロダクト情報を読み込み"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def interactive_product_input():
    """対話的にプロダクト情報を入力"""
    
    print("\n新しいプロダクトの情報を入力してください：")
    print("-"*40)
    
    product_info = {}
    
    product_info['name'] = input("プロダクト名: ").strip() or "MyProduct"
    product_info['category'] = input("カテゴリ（例: タスク管理、写真編集、etc）: ").strip() or "生産性向上"
    product_info['target'] = input("ターゲット層（例: 個人、中小企業、学生、etc）: ").strip() or "個人・中小企業"
    product_info['price'] = input("価格（例: 月額980円、無料、etc）: ").strip() or "月額980円"
    product_info['unique_value'] = input("独自の価値（例: AI自動化、シンプルUI、etc）: ").strip() or "AI機能搭載"
    
    print("\n追加情報（省略可）：")
    product_info['feature1'] = input("主要機能1: ").strip() or "自動化機能"
    product_info['feature2'] = input("主要機能2: ").strip() or "クラウド同期"
    product_info['feature3'] = input("主要機能3: ").strip() or "モバイル対応"
    
    # 成長フェーズ判定用
    users_input = input("現在のユーザー数（新規なら0）: ").strip()
    product_info['users'] = int(users_input) if users_input.isdigit() else 0
    
    return product_info

def main():
    """メイン実行関数"""
    
    print("""
╔══════════════════════════════════════════════════════════╗
║        マーケティング自動化ツール v1.0                    ║
║        - 市場分析                                        ║
║        - コンテンツ自動生成                              ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 実行モード選択
    print("\n実行モードを選択してください：")
    print("1. 新しいプロダクトを入力")
    print("2. サンプルデータで実行")
    print("3. JSONファイルから読み込み")
    
    choice = input("\n選択 (1-3): ").strip()
    
    if choice == "1":
        product_info = interactive_product_input()
    elif choice == "3":
        json_path = input("JSONファイルのパス: ").strip()
        product_info = load_product_from_json(json_path)
    else:
        # サンプルデータ
        product_info = {
            "name": "TaskMaster Pro",
            "category": "タスク管理",
            "target": "個人・中小企業",
            "price": "月額980円",
            "unique_value": "AI自動スケジューリング",
            "feature1": "AIタスク優先順位",
            "feature2": "チーム連携機能",
            "feature3": "進捗可視化"
        }
        print("\n📌 サンプルデータで実行します")
    
    # 実行確認
    print(f"\n以下の内容で実行します：")
    print(json.dumps(product_info, ensure_ascii=False, indent=2))
    
    confirm = input("\n実行しますか？ (y/n): ").strip().lower()
    if confirm != 'y':
        print("実行をキャンセルしました")
        return
    
    # マーケティング自動化実行
    try:
        market_analysis, contents = run_full_marketing_automation(product_info)
        print("\n🎉 すべての処理が正常に完了しました！")
        print(f"\n📂 結果は以下に保存されています:")
        print(f"   /Users/fukushimashouhei/dev/marketing-automation-tools/outputs/")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()