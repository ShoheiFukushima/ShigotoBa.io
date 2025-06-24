const { test, expect } = require('@playwright/test');

test.describe('Sidebar Toggle Click Debug', () => {
  
  test('should test sidebar toggle button click', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('h1:has-text("Marketing Flow Dashboard")', { timeout: 30000 });
    await page.waitForTimeout(3000);
    
    console.log('=== Before clicking sidebar toggle ===');
    
    // 現在のサイドバー状態をチェック
    const stackElementsBefore = await page.locator('text=📂 プロジェクトスタック').all();
    console.log(`Before click: プロジェクトスタック elements: ${stackElementsBefore.length}`);
    
    // サイドバートグルボタンを確認
    const toggleButton = page.locator('button[data-testid="stBaseButton-headerNoPadding"]');
    const toggleExists = await toggleButton.count();
    console.log(`Toggle button exists: ${toggleExists > 0}`);
    
    if (toggleExists > 0) {
      const isVisible = await toggleButton.isVisible();
      const isEnabled = await toggleButton.isEnabled();
      console.log(`Toggle button visible: ${isVisible}, enabled: ${isEnabled}`);
      
      // ボタンをクリック
      console.log('Clicking sidebar toggle...');
      await toggleButton.click();
      await page.waitForTimeout(2000);
      
      console.log('=== After clicking sidebar toggle ===');
      
      // クリック後のサイドバー状態をチェック
      const stackElementsAfter = await page.locator('text=📂 プロジェクトスタック').all();
      console.log(`After click: プロジェクトスタック elements: ${stackElementsAfter.length}`);
      
      if (stackElementsAfter.length > 0) {
        const firstElementVisible = await stackElementsAfter[0].isVisible();
        console.log(`First element visible: ${firstElementVisible}`);
      }
      
      // さらに詳細な検索
      const allTextElements = await page.locator('*').evaluateAll(elements => 
        elements
          .filter(el => el.textContent && el.textContent.includes('プロジェクトスタック'))
          .map(el => ({
            tag: el.tagName,
            text: el.textContent.trim(),
            visible: el.offsetParent !== null,
            className: el.className
          }))
      );
      
      console.log('Elements containing プロジェクトスタック:', allTextElements);
      
      // スクリーンショット撮影
      await page.screenshot({ path: 'debug-after-toggle-click.png', fullPage: true });
      
      // HTMLの構造を保存して確認
      const htmlContent = await page.content();
      console.log(`HTML content length after click: ${htmlContent.length}`);
      
      // サイドバー関連のdata-testidを再確認
      const sidebarElements = await page.locator('[data-testid*="sidebar"], [data-testid*="Sidebar"]').all();
      console.log(`Sidebar elements with data-testid: ${sidebarElements.length}`);
      
      for (let i = 0; i < sidebarElements.length; i++) {
        const testId = await sidebarElements[i].getAttribute('data-testid');
        const isVisible = await sidebarElements[i].isVisible();
        console.log(`Sidebar element ${i}: data-testid="${testId}", visible=${isVisible}`);
      }
    } else {
      console.log('Toggle button not found!');
      
      // 代替方法：他のトグルボタンを探す
      const allHeaderButtons = await page.locator('header button, [data-testid="stHeader"] button').all();
      console.log(`Trying all header buttons: ${allHeaderButtons.length}`);
      
      for (let i = 0; i < allHeaderButtons.length; i++) {
        const buttonText = await allHeaderButtons[i].textContent();
        console.log(`Trying header button ${i}: "${buttonText?.trim()}"`);
        
        await allHeaderButtons[i].click();
        await page.waitForTimeout(1000);
        
        const stackElements = await page.locator('text=📂 プロジェクトスタック').all();
        if (stackElements.length > 0) {
          console.log(`Success with button ${i}! Found プロジェクトスタック`);
          break;
        }
      }
    }
    
    expect(true).toBe(true);
  });
});