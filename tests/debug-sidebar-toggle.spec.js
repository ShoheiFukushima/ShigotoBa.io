const { test, expect } = require('@playwright/test');

test.describe('Sidebar Toggle Debug', () => {
  
  test('should find and click sidebar toggle', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('h1:has-text("Marketing Flow Dashboard")', { timeout: 30000 });
    await page.waitForTimeout(3000);
    
    console.log('=== Looking for sidebar toggle button ===');
    
    // 全てのボタンを確認
    const allButtons = await page.locator('button').all();
    console.log(`Total buttons: ${allButtons.length}`);
    
    for (let i = 0; i < allButtons.length; i++) {
      const buttonText = await allButtons[i].textContent();
      const buttonClass = await allButtons[i].getAttribute('class');
      const ariaLabel = await allButtons[i].getAttribute('aria-label');
      const testId = await allButtons[i].getAttribute('data-testid');
      
      console.log(`Button ${i}: text="${buttonText?.trim()}", class="${buttonClass}", aria-label="${ariaLabel}", data-testid="${testId}"`);
      
      // サイドバートグルと思われるボタンを特定
      if (
        buttonText?.trim() === '' && 
        (buttonClass?.includes('menu') || 
         ariaLabel?.includes('menu') || 
         ariaLabel?.includes('sidebar') ||
         ariaLabel?.includes('navigation') ||
         testId?.includes('menu') ||
         testId?.includes('sidebar'))
      ) {
        console.log(`*** Potential sidebar toggle found at index ${i} ***`);
        
        // ボタンをクリック
        await allButtons[i].click();
        await page.waitForTimeout(2000);
        
        // サイドバーが開いたかチェック
        const stackElements = await page.locator('text=📂 プロジェクトスタック').all();
        console.log(`After clicking: "プロジェクトスタック" elements found: ${stackElements.length}`);
        
        if (stackElements.length > 0) {
          const isVisible = await stackElements[0].isVisible();
          console.log(`First element visible: ${isVisible}`);
          
          // 成功！スクリーンショット撮影
          await page.screenshot({ path: 'sidebar-opened.png', fullPage: true });
          break;
        }
      }
    }
    
    // Header内のボタンを詳しく確認
    const headerButtons = await page.locator('header button, [data-testid="stHeader"] button').all();
    console.log(`\nHeader buttons: ${headerButtons.length}`);
    
    for (let i = 0; i < headerButtons.length; i++) {
      const buttonText = await headerButtons[i].textContent();
      const buttonClass = await headerButtons[i].getAttribute('class');
      const ariaLabel = await headerButtons[i].getAttribute('aria-label');
      console.log(`Header Button ${i}: text="${buttonText?.trim()}", class="${buttonClass}", aria-label="${ariaLabel}"`);
    }
    
    // 特定のStreamlit内部クラスを探す
    const streamlitMenuButtons = await page.locator('[class*="menu"], [class*="Menu"], [class*="sidebar"], [class*="Sidebar"]').all();
    console.log(`\nStreamlit menu-related elements: ${streamlitMenuButtons.length}`);
    
    for (let i = 0; i < Math.min(streamlitMenuButtons.length, 5); i++) {
      const tagName = await streamlitMenuButtons[i].evaluate(el => el.tagName);
      const className = await streamlitMenuButtons[i].getAttribute('class');
      console.log(`Menu element ${i}: ${tagName}.${className}`);
    }
    
    expect(true).toBe(true);
  });
  
  test('should check if sidebar content exists but is hidden', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('h1:has-text("Marketing Flow Dashboard")', { timeout: 30000 });
    await page.waitForTimeout(3000);
    
    console.log('=== Checking for hidden sidebar content ===');
    
    // サイドバー要素が存在するが非表示かチェック
    const sidebarContent = await page.locator('text=📂 プロジェクトスタック').all();
    console.log(`プロジェクトスタック elements found: ${sidebarContent.length}`);
    
    if (sidebarContent.length > 0) {
      for (let i = 0; i < sidebarContent.length; i++) {
        const isVisible = await sidebarContent[i].isVisible();
        const isAttached = await sidebarContent[i].isEnabled();
        const boundingBox = await sidebarContent[i].boundingBox();
        
        console.log(`Element ${i}: visible=${isVisible}, attached=${isAttached}, boundingBox=${JSON.stringify(boundingBox)}`);
      }
    }
    
    // st.sidebar要素を直接探す
    const stElements = await page.locator('[data-testid*="st"]').all();
    console.log(`\nAll st elements count: ${stElements.length}`);
    
    // sidebar関連のクラスやID持つ要素を探す
    const possibleSidebars = await page.evaluate(() => {
      const elements = Array.from(document.querySelectorAll('*'));
      return elements
        .filter(el => {
          const className = el.className?.toString() || '';
          const id = el.id || '';
          return className.includes('sidebar') || id.includes('sidebar') || className.includes('Sidebar');
        })
        .map(el => ({
          tag: el.tagName,
          class: el.className,
          id: el.id,
          visible: el.offsetParent !== null
        }))
        .slice(0, 10);
    });
    
    console.log('Possible sidebar elements:', possibleSidebars);
    
    expect(true).toBe(true);
  });
});