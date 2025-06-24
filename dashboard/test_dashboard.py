#!/usr/bin/env python3
"""
ダッシュボードの自動テスト・エラー検証ツール
UIを実際に起動せずにエラーを検出
"""

import sys
import os
import json
import traceback
from datetime import datetime, timedelta

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DashboardTester:
    """ダッシュボードの自動テスト"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = []
        
    def test_imports(self):
        """インポートテスト"""
        print("🔍 インポートテスト...")
        
        try:
            from tools.market_analyzer import MarketAnalyzer
            self.success.append("✅ MarketAnalyzer インポート成功")
        except Exception as e:
            self.errors.append(f"❌ MarketAnalyzer: {str(e)}")
            
        try:
            from tools.content_generator import ContentGenerator
            self.success.append("✅ ContentGenerator インポート成功")
        except Exception as e:
            self.errors.append(f"❌ ContentGenerator: {str(e)}")
            
        try:
            from tools.seasonal_analyzer import SeasonalAnalyzer
            self.success.append("✅ SeasonalAnalyzer インポート成功")
        except Exception as e:
            self.errors.append(f"❌ SeasonalAnalyzer: {str(e)}")
            
        try:
            from tools.growth_phase_strategist import GrowthPhaseStrategist, GrowthPhase
            self.success.append("✅ GrowthPhaseStrategist インポート成功")
        except Exception as e:
            self.errors.append(f"❌ GrowthPhaseStrategist: {str(e)}")
    
    def test_config_files(self):
        """設定ファイルのテスト"""
        print("\n📁 設定ファイルテスト...")
        
        # projects.json
        config_path = "dashboard/config/projects.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    projects = json.load(f)
                    
                if 'projects' in projects:
                    self.success.append(f"✅ projects.json: {len(projects['projects'])}個のプロジェクト")
                    
                    # 各プロジェクトの検証
                    for p in projects['projects']:
                        if 'path' in p:
                            if not os.path.exists(p['path']):
                                self.warnings.append(f"⚠️ プロジェクトパスが存在しません: {p['path']}")
                else:
                    self.errors.append("❌ projects.jsonに'projects'キーがありません")
                    
            except json.JSONDecodeError as e:
                self.errors.append(f"❌ projects.json JSONエラー: {str(e)}")
            except Exception as e:
                self.errors.append(f"❌ projects.json 読み込みエラー: {str(e)}")
        else:
            self.errors.append(f"❌ {config_path} が存在しません")
            
        # conversation_log.md
        log_path = "dashboard/data/conversation_log.md"
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            self.warnings.append(f"⚠️ ログディレクトリが存在しません: {log_dir}")
            
    def test_functionality(self):
        """機能テスト"""
        print("\n⚙️ 機能テスト...")
        
        # サンプルプロダクトで分析テスト
        try:
            from tools.market_analyzer import MarketAnalyzer
            analyzer = MarketAnalyzer()
            
            test_product = {
                'name': 'TestProduct',
                'category': 'テスト',
                'target': '個人',
                'price': '無料',
                'unique_value': 'テスト用',
                'users': 0
            }
            
            # outputsディレクトリ確認
            if not os.path.exists(analyzer.results_dir):
                self.warnings.append(f"⚠️ 出力ディレクトリが存在しません: {analyzer.results_dir}")
                os.makedirs(analyzer.results_dir, exist_ok=True)
                self.success.append(f"✅ 出力ディレクトリを作成: {analyzer.results_dir}")
                
            self.success.append("✅ 分析機能テスト準備完了")
            
        except Exception as e:
            self.errors.append(f"❌ 機能テストエラー: {str(e)}")
            
    def test_ui_components(self):
        """UIコンポーネントのテスト"""
        print("\n🎨 UIコンポーネントテスト...")
        
        # Streamlit設定ファイル
        streamlit_config = ".streamlit/config.toml"
        if os.path.exists(streamlit_config):
            self.success.append("✅ Streamlit設定ファイル存在")
        else:
            self.warnings.append("⚠️ Streamlit設定ファイルがありません")
            
        # 静的ファイル
        static_dirs = ["dashboard/static/css", "dashboard/static/js", "dashboard/static/images"]
        for dir_path in static_dirs:
            if not os.path.exists(dir_path):
                # 必須ではないのでwarning
                pass
                
    def test_dependencies(self):
        """依存関係のテスト"""
        print("\n📦 依存関係テスト...")
        
        required_packages = {
            'streamlit': 'Streamlit',
            'pandas': 'Pandas',
            'requests': 'Requests'
        }
        
        optional_packages = {
            'tweepy': 'Tweepy (Twitter API)',
            'schedule': 'Schedule',
            'plotly': 'Plotly'
        }
        
        # 必須パッケージ
        for package, name in required_packages.items():
            try:
                __import__(package)
                self.success.append(f"✅ {name} インストール済み")
            except ImportError:
                self.errors.append(f"❌ {name} がインストールされていません")
                
        # オプションパッケージ
        for package, name in optional_packages.items():
            try:
                __import__(package)
                self.success.append(f"✅ {name} インストール済み")
            except ImportError:
                self.warnings.append(f"⚠️ {name} がインストールされていません（オプション）")
    
    def run_all_tests(self):
        """全テスト実行"""
        print("🚀 ダッシュボード検証開始\n")
        print("="*50)
        
        self.test_dependencies()
        self.test_imports()
        self.test_config_files()
        self.test_functionality()
        self.test_ui_components()
        
        print("\n" + "="*50)
        print("📊 テスト結果サマリー\n")
        
        # 成功
        if self.success:
            print(f"✅ 成功: {len(self.success)}件")
            for s in self.success:
                print(f"  {s}")
                
        # 警告
        if self.warnings:
            print(f"\n⚠️  警告: {len(self.warnings)}件")
            for w in self.warnings:
                print(f"  {w}")
                
        # エラー
        if self.errors:
            print(f"\n❌ エラー: {len(self.errors)}件")
            for e in self.errors:
                print(f"  {e}")
        else:
            print("\n🎉 エラーなし！ダッシュボードは正常に動作するはずです。")
            
        print("\n" + "="*50)
        
        # 推奨アクション
        if self.errors or self.warnings:
            print("\n💡 推奨アクション:")
            
            if any("パッケージ" in e for e in self.errors):
                print("- 必要なパッケージをインストール: pip install streamlit pandas")
                
            if any("ディレクトリ" in w for w in self.warnings):
                print("- 不足しているディレクトリは自動作成されます")
                
            if any("プロジェクトパス" in w for w in self.warnings):
                print("- プロジェクトパスは実際の環境に合わせて調整されます")
        
        return len(self.errors) == 0


def main():
    """メイン実行"""
    tester = DashboardTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ ダッシュボードを起動する準備ができています！")
        print("\n実行コマンド:")
        print("cd /Users/fukushimashouhei/dev/marketing-automation-tools")
        print("python3 quick_start.py")
    else:
        print("\n⚠️ エラーを修正してから起動してください。")
        
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())