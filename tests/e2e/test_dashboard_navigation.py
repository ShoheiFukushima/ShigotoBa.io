#!/usr/bin/env python3
"""
ダッシュボード4構成のE2Eテスト
ナビゲーション、ページ遷移、エラーチェック
"""

import pytest
from playwright.sync_api import Page, expect
import time

class TestDashboardNavigation:
    """ダッシュボードナビゲーションのテスト"""
    
    base_url = "http://localhost:8501"
    
    def test_home_page_loads(self, page: Page):
        """ホームページが正しく読み込まれることを確認"""
        page.goto(self.base_url)
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # タイトル確認
        expect(page).to_have_title("マーケティング自動化ダッシュボード")
        
        # メインヘッダーの確認
        header = page.locator("h1.greeting")
        expect(header).to_be_visible()
        
        # 統計カードの確認
        stats = page.locator(".stat-card")
        expect(stats).to_have_count(5)
        
        # クイックアクセスボタンの確認
        buttons = page.locator("button").filter(has_text="管理室")
        expect(buttons.first).to_be_visible()
    
    def test_navigation_to_project_management(self, page: Page):
        """プロジェクト管理室への遷移テスト"""
        page.goto(self.base_url)
        page.wait_for_load_state("networkidle")
        
        # プロジェクト管理室ボタンをクリック
        page.click("button:has-text('プロジェクト管理室')")
        time.sleep(2)
        
        # ページ遷移の確認
        expect(page).to_have_url(f"{self.base_url}/project_management.py")
        
        # パンくずナビゲーションの確認
        breadcrumb = page.locator(".breadcrumb")
        expect(breadcrumb).to_be_visible()
        
        # 戻るボタンの確認
        back_button = page.locator("button:has-text('ダッシュボードに戻る')")
        expect(back_button).to_be_visible()
    
    def test_navigation_to_development_room(self, page: Page):
        """開発室への遷移テスト"""
        page.goto(self.base_url)
        page.wait_for_load_state("networkidle")
        
        # 開発室ボタンをクリック
        page.click("button:has-text('開発室')")
        time.sleep(2)
        
        # ページ遷移の確認
        expect(page).to_have_url(f"{self.base_url}/development_room.py")
        
        # Geminiカードの確認
        gemini_cards = page.locator(".gemini-card")
        expect(gemini_cards.first).to_be_visible()
    
    def test_create_new_project(self, page: Page):
        """新規プロジェクト作成のテスト"""
        page.goto(f"{self.base_url}/development_room.py")
        page.wait_for_load_state("networkidle")
        
        # プロダクト名入力
        page.fill("input[placeholder='例: TaskFlow AI']", "テストプロダクト")
        
        # カテゴリ選択
        page.select_option("select", "Webアプリケーション")
        
        # ターゲット層入力
        page.fill("textarea[placeholder*='中小企業']", "テストターゲット")
        
        # フォーム送信
        page.click("button:has-text('プロジェクトを作成')")
        time.sleep(2)
        
        # 成功メッセージの確認
        success_message = page.locator(".stSuccess")
        expect(success_message).to_be_visible()
    
    def test_project_detail_navigation(self, page: Page):
        """プロジェクト詳細画面への遷移テスト"""
        # まずプロジェクトを作成
        self.test_create_new_project(page)
        
        # プロジェクト管理室へ移動
        page.goto(f"{self.base_url}/project_management.py")
        page.wait_for_load_state("networkidle")
        
        # 詳細表示ボタンをクリック
        detail_button = page.locator("button:has-text('詳細表示')").first
        if detail_button.is_visible():
            detail_button.click()
            time.sleep(2)
            
            # プロジェクト詳細ページの確認
            expect(page).to_have_url(f"{self.base_url}/project_detail.py")
            
            # パンくずナビゲーションの確認
            breadcrumb = page.locator("div").filter(has_text="プロジェクト室")
            expect(breadcrumb).to_be_visible()
    
    def test_sidebar_navigation(self, page: Page):
        """サイドバーナビゲーションのテスト"""
        page.goto(self.base_url)
        page.wait_for_load_state("networkidle")
        
        # サイドバーが閉じている場合は開く
        sidebar_toggle = page.locator("button[aria-label='Open sidebar']")
        if sidebar_toggle.is_visible():
            sidebar_toggle.click()
            time.sleep(1)
        
        # サイドバーのクイックアクションボタン確認
        sidebar_button = page.locator("section[data-testid='stSidebar'] button:has-text('新規プロジェクト')")
        expect(sidebar_button).to_be_visible()
    
    def test_breadcrumb_navigation(self, page: Page):
        """パンくずナビゲーションのテスト"""
        # プロジェクト詳細ページへ
        page.goto(f"{self.base_url}/project_detail.py")
        page.wait_for_load_state("networkidle")
        
        # パンくずリンクの確認
        breadcrumb_home = page.locator("a:has-text('ダッシュボード')")
        breadcrumb_management = page.locator("a:has-text('プロジェクト管理室')")
        
        expect(breadcrumb_home).to_be_visible()
        expect(breadcrumb_management).to_be_visible()
    
    def test_error_handling(self, page: Page):
        """エラーハンドリングのテスト"""
        # 存在しないページへのアクセス
        page.goto(f"{self.base_url}/nonexistent_page.py")
        page.wait_for_load_state("networkidle")
        
        # エラーメッセージまたはリダイレクトの確認
        error_message = page.locator("text=Error")
        home_redirect = page.locator("h1.greeting")
        
        # エラーメッセージかホームへのリダイレクトを確認
        assert error_message.is_visible() or home_redirect.is_visible()
    
    def test_responsive_layout(self, page: Page):
        """レスポンシブレイアウトのテスト"""
        # モバイルサイズ
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(self.base_url)
        page.wait_for_load_state("networkidle")
        
        # モバイルでも主要要素が表示されることを確認
        header = page.locator("h1.greeting")
        expect(header).to_be_visible()
        
        # デスクトップサイズ
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.reload()
        page.wait_for_load_state("networkidle")
        
        # デスクトップレイアウトの確認
        columns = page.locator("[data-testid='column']")
        expect(columns.first).to_be_visible()


class TestProjectWorkflow:
    """プロジェクトワークフローのE2Eテスト"""
    
    base_url = "http://localhost:8501"
    
    def test_complete_project_workflow(self, page: Page):
        """プロジェクト作成から詳細確認までの完全なワークフロー"""
        # 1. ホームページから開始
        page.goto(self.base_url)
        page.wait_for_load_state("networkidle")
        
        # 2. 開発室へ移動
        page.click("button:has-text('開発室')")
        time.sleep(2)
        
        # 3. 新規プロジェクト作成
        test_project_name = f"E2Eテストプロジェクト_{int(time.time())}"
        page.fill("input[placeholder='例: TaskFlow AI']", test_project_name)
        page.select_option("select", "AIツール")
        page.fill("textarea[placeholder*='中小企業']", "E2Eテスト用ターゲット")
        page.fill("textarea[placeholder*='AI による']", "E2Eテスト用の独自価値")
        
        page.click("button:has-text('プロジェクトを作成')")
        time.sleep(2)
        
        # 4. プロジェクト管理室で確認
        page.click("button:has-text('プロジェクト管理室へ')")
        time.sleep(2)
        
        # 作成したプロジェクトが表示されることを確認
        project_card = page.locator(f"text={test_project_name}")
        expect(project_card).to_be_visible()
        
        # 5. プロジェクト詳細を確認
        page.click(f"button:has-text('詳細表示'):near(text={test_project_name})")
        time.sleep(2)
        
        # プロジェクト詳細ページでの表示確認
        project_title = page.locator(f"text={test_project_name}")
        expect(project_title).to_be_visible()
        
        # 6. ホームに戻る
        page.click("a:has-text('ダッシュボード')")
        time.sleep(2)
        
        # ホームページに戻ったことを確認
        expect(page).to_have_url(self.base_url)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])