const { test, expect } = require('@playwright/test');

test.describe('シンプルナビゲーションテスト', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('h1', { timeout: 30000 });
    await page.waitForTimeout(2000);
  });

  test('開発室ページへの遷移', async ({ page }) => {
    // 開発室ボタンをクリック
    const devRoomButton = page.locator('button').filter({ hasText: '開発室' });
    await expect(devRoomButton).toBeVisible();
    await devRoomButton.click();
    
    // ページ遷移の確認
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    // URLまたはページタイトルで遷移確認
    const currentUrl = page.url();
    expect(currentUrl).toContain('development_room');
  });

  test('プロダクト管理ページへの遷移', async ({ page }) => {
    // プロダクト管理ボタンをクリック  
    const productButton = page.locator('button').filter({ hasText: 'プロダクト' });
    await expect(productButton).toBeVisible();
    await productButton.click();
    
    // ページ遷移の確認
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    const currentUrl = page.url();
    expect(currentUrl).toContain('product_management');
  });

  test('パフォーマンスダッシュボードへの遷移', async ({ page }) => {
    // パフォーマンスボタンをクリック
    const performanceButton = page.locator('button').filter({ hasText: 'パフォーマンス' });
    await expect(performanceButton).toBeVisible();
    await performanceButton.click();
    
    // ページ遷移の確認
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    const currentUrl = page.url();
    expect(currentUrl).toContain('performance_dashboard');
  });

  test('AI Creative Studioへの遷移', async ({ page }) => {
    // AI Creative Studioボタンをクリック
    const aiStudioButton = page.locator('button').filter({ hasText: 'AI Creative' });
    await expect(aiStudioButton).toBeVisible();
    await aiStudioButton.click();
    
    // ページ遷移の確認
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    const currentUrl = page.url();
    expect(currentUrl).toContain('ai_creative_studio');
  });

  test('サイドバー新規プロジェクトボタンの動作', async ({ page }) => {
    // サイドバーの新規プロジェクトボタンをクリック
    const newProjectButton = page.locator('button').filter({ hasText: '新規プロジェクト' });
    await expect(newProjectButton).toBeVisible();
    await newProjectButton.click();
    
    // ページ遷移の確認
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    const currentUrl = page.url();
    expect(currentUrl).toContain('development_room');
  });

});