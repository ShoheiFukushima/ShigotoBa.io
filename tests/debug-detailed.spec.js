const { test, expect } = require('@playwright/test');

test.describe('Detailed Debug Tests', () => {
  
  test('should wait for full app load and debug elements', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Streamlitアプリのタイトルを待つ
    await page.waitForSelector('h1:has-text("Marketing Flow Dashboard")', { timeout: 30000 });
    await page.waitForTimeout(3000);  // さらに長く待機
    
    console.log('=== After full load ===');
    
    // 全てのボタンを再確認
    const buttons = await page.locator('button').all();
    console.log('Total buttons found after full load:', buttons.length);
    
    for (let i = 0; i < Math.min(buttons.length, 15); i++) {
      const buttonText = await buttons[i].textContent();
      const buttonClass = await buttons[i].getAttribute('class');
      console.log(`Button ${i}: "${buttonText}" | Class: ${buttonClass}`);
    }
    
    // div要素を確認
    const divElements = await page.locator('div').all();
    console.log('Total div elements:', divElements.length);
    
    // プロジェクト管理関連を確認
    const projectText = await page.locator('text=プロジェクト管理').all();
    console.log('Project management text elements:', projectText.length);
    
    // エクスパンダーを確認
    const expanders = await page.locator('[data-testid*="expander"]').all();
    console.log('Expander elements found:', expanders.length);
    
    // stの付くdata-testidを確認
    const stElements = await page.locator('[data-testid*="st"]').all();
    console.log('Elements with st* data-testid:', stElements.length);
    
    for (let i = 0; i < Math.min(stElements.length, 10); i++) {
      const testId = await stElements[i].getAttribute('data-testid');
      console.log(`ST Element ${i}: data-testid="${testId}"`);
    }
    
    // プロジェクト作成ボタンを探す
    const createButtons = await page.locator('text=新規作成').all();
    console.log('Create button elements found:', createButtons.length);
    
    // フローステージボタンを探す
    const stageButtons = await page.locator('button').filter({ hasText: 'プロダクト入力' }).all();
    console.log('Stage button elements found:', stageButtons.length);
    
    // CSS classes with progress
    const progressClasses = await page.locator('[class*="progress"]').all();
    console.log('Elements with progress in class:', progressClasses.length);
    
    // 全HTML構造をファイルに保存
    const htmlContent = await page.content();
    console.log('HTML content length:', htmlContent.length);
    
    // スクリーンショットを撮影
    await page.screenshot({ path: 'debug-full-app.png', fullPage: true });
    
    expect(true).toBe(true);
  });
});