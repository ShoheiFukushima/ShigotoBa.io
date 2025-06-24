const { test, expect } = require('@playwright/test');

test.describe('ページ機能性テスト', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('h1', { timeout: 30000 });
    await page.waitForTimeout(2000);
  });

  test('開発室ページの機能確認', async ({ page }) => {
    // 開発室ページに移動
    await page.locator('button').filter({ hasText: '開発室' }).click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    // ページタイトルの確認
    const pageTitle = page.locator('h1');
    await expect(pageTitle).toBeVisible();
    
    // フォーム要素の存在確認
    const inputs = page.locator('input, textarea, select');
    const inputCount = await inputs.count();
    expect(inputCount).toBeGreaterThan(0);
    
    // ボタンの存在確認
    const buttons = page.locator('button');
    const buttonCount = await buttons.count();
    expect(buttonCount).toBeGreaterThan(0);
  });

  test('プロダクト管理ページの機能確認', async ({ page }) => {
    // プロダクト管理ページに移動
    await page.locator('button').filter({ hasText: 'プロダクト' }).click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    // ページタイトルの確認
    const pageTitle = page.locator('h1');
    await expect(pageTitle).toBeVisible();
    
    // プロダクト管理機能の確認
    const productElements = page.locator('text=プロダクト');
    await expect(productElements.first()).toBeVisible();
  });

  test('パフォーマンスダッシュボードの表示確認', async ({ page }) => {
    // パフォーマンスダッシュボードに移動
    await page.locator('button').filter({ hasText: 'パフォーマンス' }).click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(5000); // パフォーマンスページは重いので少し長めに待機
    
    // ページが正常に読み込まれたか確認
    const pageContent = page.locator('body');
    await expect(pageContent).toBeVisible();
    
    // エラーがないか確認（エラーメッセージが表示されていないこと）
    const errorMessages = page.locator('text=Error, text=エラー, text=traceback');
    const errorCount = await errorMessages.count();
    expect(errorCount).toBe(0);
  });

  test('AI Creative Studioの基本機能確認', async ({ page }) => {
    // AI Creative Studioに移動
    await page.locator('button').filter({ hasText: 'AI Creative' }).click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    // ページタイトルの確認
    const pageTitle = page.locator('h1');
    await expect(pageTitle).toBeVisible();
    
    // AI機能の確認
    const aiElements = page.locator('text=AI, text=Creative, text=Studio');
    const aiElementCount = await aiElements.count();
    expect(aiElementCount).toBeGreaterThan(0);
  });

  test('ホーム画面のメトリクス機能確認', async ({ page }) => {
    // ホーム画面でメトリクスの値を確認
    const metrics = [
      'アクティブプロジェクト',
      '未完了タスク',
      '今週の成果',
      '効率スコア'
    ];
    
    for (const metric of metrics) {
      const metricElement = page.locator(`text=${metric}`);
      await expect(metricElement).toBeVisible();
      
      // メトリクスの値が表示されているか確認
      const metricValue = metricElement.locator('xpath=following-sibling::*[1]');
      await expect(metricValue).toBeVisible();
    }
  });

  test('サイドバーの統計情報確認', async ({ page }) => {
    // サイドバーの統計情報を確認
    const sidebarStats = [
      '完了タスク',
      '生成コンテンツ',
      '投稿数'
    ];
    
    for (const stat of sidebarStats) {
      const statElement = page.locator(`text=${stat}`).first();
      await expect(statElement).toBeVisible();
    }
    
    // 通知セクションの確認
    const notificationHeader = page.locator('text=🔔 通知');
    await expect(notificationHeader).toBeVisible();
  });

  test('レスポンシブデザインの確認', async ({ page }) => {
    // モバイルサイズに変更
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(2000);
    
    // ページが適切に表示されるか確認
    const mainContent = page.locator('h1');
    await expect(mainContent).toBeVisible();
    
    // デスクトップサイズに戻す
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.waitForTimeout(2000);
    
    // レイアウトが適切に戻るか確認
    await expect(mainContent).toBeVisible();
  });

});