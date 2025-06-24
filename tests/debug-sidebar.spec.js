const { test, expect } = require('@playwright/test');

test.describe('Sidebar Structure Debug', () => {
  
  test('should search for sidebar and project stack elements', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('h1:has-text("Marketing Flow Dashboard")', { timeout: 30000 });
    await page.waitForTimeout(3000);
    
    console.log('=== Searching for sidebar elements ===');
    
    // サイドバー関連のdata-testidを探す
    const sidebarTestIds = ['stSidebar', 'stSidebarNav', 'stSidebarContent'];
    for (const testId of sidebarTestIds) {
      const elements = await page.locator(`[data-testid="${testId}"]`).all();
      console.log(`${testId}: ${elements.length} elements found`);
    }
    
    // プロジェクトスタック関連のテキストを探す
    const projectTexts = [
      'プロジェクトスタック',
      'フロー全体図', 
      'プロジェクトがありません',
      'プロジェクト管理'
    ];
    
    for (const text of projectTexts) {
      const elements = await page.locator(`text=${text}`).all();
      console.log(`"${text}": ${elements.length} elements found`);
      
      if (elements.length > 0) {
        for (let i = 0; i < elements.length; i++) {
          const isVisible = await elements[i].isVisible();
          const parentTag = await elements[i].evaluate(el => el.parentElement?.tagName);
          console.log(`  Element ${i}: visible=${isVisible}, parent=${parentTag}`);
        }
      }
    }
    
    // Streamlitのカラム構造を確認
    const columns = await page.locator('[data-testid*="column"]').all();
    console.log(`Streamlit columns found: ${columns.length}`);
    
    // 全てのテキスト要素を確認（上位20個）
    const allTextElements = await page.locator('*').evaluateAll(elements => 
      elements
        .filter(el => el.textContent && el.textContent.trim().length > 0)
        .map(el => ({
          tag: el.tagName,
          text: el.textContent.trim().substring(0, 50),
          visible: el.offsetParent !== null
        }))
        .slice(0, 30)
    );
    
    console.log('=== All text elements (first 30) ===');
    allTextElements.forEach((el, i) => {
      console.log(`${i}: ${el.tag} "${el.text}" visible=${el.visible}`);
    });
    
    // HTMLの構造をファイルに保存
    const htmlContent = await page.content();
    console.log('Full HTML saved to debug-sidebar.html');
    
    // スクリーンショット
    await page.screenshot({ path: 'debug-sidebar.png', fullPage: true });
    
    expect(true).toBe(true);
  });
  
  test('should check for hidden or collapsed sidebar', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('h1:has-text("Marketing Flow Dashboard")', { timeout: 30000 });
    await page.waitForTimeout(3000);
    
    console.log('=== Checking for hidden/collapsed sidebar ===');
    
    // サイドバートグルボタンを探す
    const toggleButtons = await page.locator('button').all();
    for (let i = 0; i < toggleButtons.length; i++) {
      const buttonText = await toggleButtons[i].textContent();
      const buttonClass = await toggleButtons[i].getAttribute('class');
      const ariaLabel = await toggleButtons[i].getAttribute('aria-label');
      
      if (buttonText === '' && (buttonClass?.includes('menu') || ariaLabel?.includes('menu'))) {
        console.log(`Potential sidebar toggle button found: class="${buttonClass}", aria-label="${ariaLabel}"`);
        
        // ボタンをクリックしてサイドバーを開く
        await toggleButtons[i].click();
        await page.waitForTimeout(1000);
        
        // プロジェクトスタックを再度確認
        const stackElements = await page.locator('text=プロジェクトスタック').all();
        console.log(`After clicking toggle: "プロジェクトスタック" elements: ${stackElements.length}`);
        
        break;
      }
    }
    
    // 全体のCSS構造を確認
    const appContainer = await page.locator('[data-testid="stApp"]').first();
    const appHTML = await appContainer.innerHTML();
    console.log(`App container HTML length: ${appHTML.length}`);
    
    expect(true).toBe(true);
  });
});