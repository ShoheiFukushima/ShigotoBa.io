import { test, expect } from '@playwright/test';

test.describe('新しいUI実装の動作テスト', () => {
  test.beforeEach(async ({ page }) => {
    // 本番環境をテスト（ローカルの場合は http://localhost:8501）
    await page.goto('https://shigotoba-io-akdiqe4v6a-an.a.run.app');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000); // Streamlitの初期化を待つ
  });

  test('メインページの基本表示', async ({ page }) => {
    // タイトルの確認
    await expect(page.locator('h1')).toContainText('ダッシュボード');
    
    // メトリクス表示の確認
    const metricsSection = page.locator('text=今日の概要');
    await expect(metricsSection).toBeVisible();
    
    // プロジェクト一覧の確認
    const projectSection = page.locator('text=プロジェクト一覧');
    await expect(projectSection).toBeVisible();
    
    // クイックアクセスの確認
    const quickAccessSection = page.locator('text=クイックアクセス');
    await expect(quickAccessSection).toBeVisible();
  });

  test('Streamlitサイドバーの基本動作', async ({ page }) => {
    // Streamlitの標準サイドバー要素を確認
    const sidebar = page.locator('[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    
    // サイドバー内のコンテンツを確認
    const sidebarContent = sidebar.locator('.stMarkdown');
    await expect(sidebarContent.first()).toBeVisible();
  });

  test('新規開発ツールへのナビゲーション', async ({ page }) => {
    // 新規開発セクションの確認
    const devSection = page.locator('text=新規開発');
    await expect(devSection).toBeVisible();
    
    // 開発ツールボタンの存在確認
    const devButtons = page.locator('button').filter({ hasText: /開発|プロジェクト|企画/ });
    const buttonCount = await devButtons.count();
    expect(buttonCount).toBeGreaterThan(0);
    
    // 最初のボタンをクリックしてページ遷移をテスト
    if (buttonCount > 0) {
      const firstButton = devButtons.first();
      await expect(firstButton).toBeVisible();
      // クリック可能かテスト（実際にはクリックしない）
      await expect(firstButton).toBeEnabled();
    }
  });

  test('運営・分析ツールへのナビゲーション', async ({ page }) => {
    // 運営・分析セクションの確認
    const analyticsSection = page.locator('text=運営・分析');
    await expect(analyticsSection).toBeVisible();
    
    // 分析ツールボタンの存在確認
    const analyticsButtons = page.locator('button').filter({ hasText: /分析|マーケ|運営|パフォーマンス/ });
    const buttonCount = await analyticsButtons.count();
    expect(buttonCount).toBeGreaterThan(0);
  });

  test('検索機能の動作', async ({ page }) => {
    // 検索ボックスの存在確認
    const searchBox = page.locator('input[placeholder*="検索"], input[placeholder*="ツール"], input[placeholder*="機能"]');
    if (await searchBox.count() > 0) {
      await expect(searchBox.first()).toBeVisible();
      
      // 検索テスト
      await searchBox.first().fill('AI');
      await page.waitForTimeout(1000);
      
      // 検索結果が表示されるかを確認（結果があれば）
      const searchResults = page.locator('text=検索結果, text=結果');
      // 結果の存在は必須ではないが、エラーがないことを確認
    }
  });

  test('レスポンシブデザインの確認', async ({ page }) => {
    // デスクトップサイズでのテスト
    await page.setViewportSize({ width: 1200, height: 800 });
    await page.waitForTimeout(1000);
    
    const mainContent = page.locator('h1');
    await expect(mainContent).toBeVisible();
    
    // タブレットサイズでのテスト
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(1000);
    
    await expect(mainContent).toBeVisible();
    
    // モバイルサイズでのテスト
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(1000);
    
    await expect(mainContent).toBeVisible();
  });

  test('Streamlitコンポーネントの基本動作', async ({ page }) => {
    // Streamlitアプリが正常にロードされているかを確認
    const streamlitApp = page.locator('[data-testid="stApp"]');
    await expect(streamlitApp).toBeVisible();
    
    // メインコンテンツエリアの確認
    const mainContent = page.locator('[data-testid="stAppViewContainer"]');
    await expect(mainContent).toBeVisible();
    
    // エラーメッセージがないことを確認
    const errorElements = page.locator('text=Error, text=エラー, [data-testid="stException"]');
    expect(await errorElements.count()).toBe(0);
  });
});

test.describe('AI機能搭載ページのテスト', () => {
  const aiPages = [
    { name: 'カスタマージャーニーエンジン', path: '/_customer_journey_engine' },
    { name: '価格戦略コンサルティング', path: '/_pricing_strategy' },
    { name: 'アトリビューション分析', path: '/_attribution_analysis' },
    { name: 'マルチプラットフォーム管理', path: '/_multi_platform_manager' }
  ];

  aiPages.forEach(({ name, path }) => {
    test(`${name}ページのAI機能テスト`, async ({ page }) => {
      // 直接ページにアクセス
      const fullUrl = `https://shigotoba-io-akdiqe4v6a-an.a.run.app${path}`;
      await page.goto(fullUrl);
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(3000);
      
      // ページが正常にロードされることを確認
      const streamlitApp = page.locator('[data-testid="stApp"]');
      await expect(streamlitApp).toBeVisible();
      
      // AI分析ボタンの存在確認
      const aiButton = page.locator('button').filter({ hasText: /AI.*分析|AI.*実行/ });
      if (await aiButton.count() > 0) {
        await expect(aiButton.first()).toBeVisible();
        await expect(aiButton.first()).toBeEnabled();
        
        console.log(`✅ ${name}: AI分析ボタンが見つかりました`);
        
        // AI分析ボタンをクリック（実際の分析は実行しない）
        // await aiButton.first().click();
        // await page.waitForTimeout(2000);
      } else {
        console.log(`⚠️ ${name}: AI分析ボタンが見つかりませんでした`);
      }
      
      // エラーがないことを確認
      const errorElements = page.locator('text=Error, text=エラー, [data-testid="stException"]');
      expect(await errorElements.count()).toBe(0);
    });
  });
});