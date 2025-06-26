import { test, expect } from '@playwright/test';

test.describe('強化版サイドバー 簡易テスト', () => {
  test('基本動作確認', async ({ page }) => {
    await page.goto('http://localhost:8501');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    // カスタムHTMLコンポーネントが存在するかチェック
    const hasCustomComponent = await page.evaluate(() => {
      const iframe = document.querySelector('iframe[title*="streamlit"]');
      if (iframe) {
        try {
          const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
          return iframeDoc.querySelector('#sidebarContainer') !== null;
        } catch (e) {
          // Cross-origin制限の場合
          return false;
        }
      }
      // 直接DOMにある場合
      return document.querySelector('#sidebarContainer') !== null;
    });
    
    console.log('カスタムコンポーネント検出:', hasCustomComponent);
    
    // Streamlitのサイドバーをチェック
    const sidebar = await page.locator('section[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    
    // プロジェクト選択ドロップダウン
    const projectSelector = await page.locator('[data-testid="stSelectbox"]').first();
    await expect(projectSelector).toBeVisible();
    
    console.log('テスト完了');
  });
});