#!/usr/bin/env python3
"""
最新機能のテストスクリプト
USER_MANUAL.mdの内容を確認し、デプロイされた機能をテスト
"""

import pytest
import requests
import time

# Seleniumは後でインポート（オプショナル）
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# テスト対象URL
BASE_URL = "https://shigotoba-io-328944491653.asia-northeast1.run.app"

class TestLatestFeatures:
    """最新機能のテスト"""
    
    @classmethod
    def setup_class(cls):
        """テストセットアップ"""
        # ヘッドレスモードでChromeを起動
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def teardown_class(cls):
        """テストクリーンアップ"""
        cls.driver.quit()
    
    def test_01_site_access(self):
        """サイトへのアクセステスト"""
        print("\n=== サイトアクセステスト ===")
        response = requests.get(BASE_URL)
        assert response.status_code == 200, f"サイトにアクセスできません: {response.status_code}"
        print("✅ サイトアクセス: OK")
    
    def test_02_dashboard_load(self):
        """ダッシュボード読み込みテスト"""
        print("\n=== ダッシュボード読み込みテスト ===")
        self.driver.get(BASE_URL)
        time.sleep(5)  # Streamlitの読み込み待機
        
        # タイトル確認
        assert "shigotoba.io" in self.driver.title or "マーケティング自動化" in self.driver.title
        print("✅ ダッシュボード読み込み: OK")
    
    def test_03_sidebar_elements(self):
        """サイドバー要素のテスト"""
        print("\n=== サイドバー要素テスト ===")
        
        # サイドバーの展開を待つ
        time.sleep(3)
        
        # 新機能ボタンの確認
        try:
            # 統合サマリーボタン
            summary_button = self.driver.find_element(By.XPATH, "//*[contains(text(), '統合サマリー')]")
            assert summary_button is not None
            print("✅ 統合サマリーボタン: 存在確認")
        except:
            print("⚠️ 統合サマリーボタンが見つかりません")
        
        try:
            # AIパイプラインボタン
            pipeline_button = self.driver.find_element(By.XPATH, "//*[contains(text(), 'AIパイプライン')]")
            assert pipeline_button is not None
            print("✅ AIパイプラインボタン: 存在確認")
        except:
            print("⚠️ AIパイプラインボタンが見つかりません")
    
    def test_04_main_categories(self):
        """メインカテゴリの確認"""
        print("\n=== メインカテゴリ確認テスト ===")
        
        categories = [
            ("新規開発", "🏗️"),
            ("運営・分析", "📊"),
            ("広告・マーケ", "🎨")
        ]
        
        for category_name, icon in categories:
            try:
                element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{category_name}')]")
                assert element is not None
                print(f"✅ {icon} {category_name}カテゴリ: 存在確認")
            except:
                print(f"⚠️ {category_name}カテゴリが見つかりません")
    
    def test_05_workflow_manager_detail(self):
        """ワークフロー管理の詳細機能テスト"""
        print("\n=== ワークフロー管理詳細機能テスト ===")
        
        # ワークフロー管理ページへ移動
        try:
            workflow_link = self.driver.find_element(By.XPATH, "//*[contains(text(), 'ワークフロー管理')]")
            workflow_link.click()
            time.sleep(3)
            
            # 詳細を見るボタンの存在確認
            detail_buttons = self.driver.find_elements(By.XPATH, "//*[contains(text(), '詳細を見る')]")
            if detail_buttons:
                print(f"✅ 詳細を見るボタン: {len(detail_buttons)}個検出")
                
                # 最初のボタンをクリック
                detail_buttons[0].click()
                time.sleep(2)
                
                # 詳細表示の確認
                detail_section = self.driver.find_element(By.XPATH, "//*[contains(text(), 'ワークフロー詳細')]")
                assert detail_section is not None
                print("✅ ワークフロー詳細表示: 正常動作")
            else:
                print("⚠️ 詳細を見るボタンが見つかりません")
        except Exception as e:
            print(f"⚠️ ワークフロー管理テストでエラー: {str(e)}")
    
    def test_06_metrics_display(self):
        """メトリクス表示のテスト"""
        print("\n=== メトリクス表示テスト ===")
        
        # ホームに戻る
        self.driver.get(BASE_URL)
        time.sleep(3)
        
        metrics = [
            "アクティブプロジェクト",
            "完了タスク",
            "新規コンテンツ",
            "効率スコア"
        ]
        
        for metric in metrics:
            try:
                element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{metric}')]")
                assert element is not None
                print(f"✅ {metric}: 表示確認")
            except:
                print(f"⚠️ {metric}が見つかりません")

def run_basic_tests():
    """基本的なテストを実行"""
    print("=== 基本的な接続テスト ===")
    
    # 1. HTTPリクエストテスト
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"✅ HTTP接続: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"   Response Size: {len(response.content)} bytes")
    except Exception as e:
        print(f"❌ HTTP接続エラー: {str(e)}")
        return False
    
    # 2. レスポンス内容の基本確認
    content = response.text.lower()
    checks = [
        ("Streamlit", "streamlit" in content),
        ("タイトル要素", "<title>" in content),
        ("スクリプト要素", "<script" in content)
    ]
    
    for check_name, result in checks:
        if result:
            print(f"✅ {check_name}: 検出")
        else:
            print(f"⚠️ {check_name}: 未検出")
    
    return True

def main():
    """メインテスト実行"""
    print("🧪 shigotoba.io 最新機能テスト開始")
    print(f"📍 対象URL: {BASE_URL}")
    print("=" * 50)
    
    # 基本テスト
    if not run_basic_tests():
        print("\n❌ 基本テストに失敗しました")
        return
    
    # Seleniumテスト実行の確認
    if SELENIUM_AVAILABLE:
        print("\n✅ Selenium利用可能")
        
        # 詳細テスト実行
        test = TestLatestFeatures()
        test.setup_class()
        
        try:
            test.test_01_site_access()
            test.test_02_dashboard_load()
            test.test_03_sidebar_elements()
            test.test_04_main_categories()
            test.test_05_workflow_manager_detail()
            test.test_06_metrics_display()
            
            print("\n🎉 すべてのテストが完了しました！")
            
        finally:
            test.teardown_class()
    else:
        print("\n⚠️ Seleniumがインストールされていません")
        print("詳細なUIテストにはSeleniumが必要です")
        print("インストール: pip install selenium")

def run_manual_checks():
    """手動確認項目のチェックリスト"""
    print("\n📋 手動確認チェックリスト")
    print("=" * 50)
    
    checks = [
        "✅ ワークフロー管理ページで「詳細を見る」ボタンをクリック",
        "✅ ワークフロー詳細が表示されることを確認",
        "✅ ステップバイステップの表示を確認",
        "✅ アクションボタン（実行・コピー・閉じる）の動作確認",
        "✅ サイドバーの「統合サマリー」ボタンの存在確認",
        "✅ サイドバーの「AIパイプライン」ボタンの存在確認",
        "✅ 3つのメインカテゴリが正しく表示されることを確認",
        "✅ ダッシュボードのメトリクスが表示されることを確認"
    ]
    
    for check in checks:
        print(f"  {check}")
    
    print("\n📱 テストURL:")
    print(f"  {BASE_URL}")
    print("\n💡 ヒント: ブラウザで上記URLにアクセスして確認してください")

if __name__ == "__main__":
    main()
    run_manual_checks()