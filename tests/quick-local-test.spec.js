import { test, expect } from '@playwright/test';

test.describe('ローカル開発環境の動作確認', () => {
  test('本番環境での基本動作確認', async ({ page }) => {
    // 本番URLへのアクセス
    await page.goto('https://shigotoba-io-akdiqe4v6a-an.a.run.app');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // ページタイトルの確認
    const title = await page.title();
    expect(title).toContain('shigotoba.io');
    
    // メインコンテンツの確認
    const mainHeading = page.locator('h1').first();
    await expect(mainHeading).toBeVisible();
    
    // Streamlitアプリの基本要素確認
    const streamlitApp = page.locator('[data-testid="stApp"]');
    await expect(streamlitApp).toBeVisible();
    
    // エラーなしで実行されていることを確認
    const errors = page.locator('[data-testid="stException"]');
    expect(await errors.count()).toBe(0);
    
    console.log('✅ 本番環境で正常動作確認');
  });
  
  test('AI機能ページへの直接アクセステスト', async ({ page }) => {
    const testPages = [
      '/pages/_customer_journey_engine',
      '/pages/_pricing_strategy', 
      '/pages/_attribution_analysis',
      '/pages/_multi_platform_manager'
    ];
    
    for (const pagePath of testPages) {
      await page.goto(`https://shigotoba-io-akdiqe4v6a-an.a.run.app${pagePath}`);
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      // ページが正常にロードされることを確認
      const streamlitApp = page.locator('[data-testid="stApp"]');
      await expect(streamlitApp).toBeVisible();
      
      // エラーがないことを確認
      const errors = page.locator('[data-testid="stException"]');
      expect(await errors.count()).toBe(0);
      
      console.log(`✅ ${pagePath} ページ正常動作`);
    }
  });
  
  test('パフォーマンス基本チェック', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('https://shigotoba-io-akdiqe4v6a-an.a.run.app');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    console.log(`📊 ページロード時間: ${loadTime}ms`);
    
    // 10秒以内のロードを期待（Cloud Runの起動時間を考慮）
    expect(loadTime).toBeLessThan(10000);
    
    // メインコンテンツが表示されていることを確認
    const mainContent = page.locator('h1');
    await expect(mainContent).toBeVisible();
    
    console.log('✅ パフォーマンス基本チェック通過');
  });
});