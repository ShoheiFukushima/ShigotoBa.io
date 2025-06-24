const { test, expect } = require('@playwright/test');

test.describe('DOM Structure Debug', () => {
  
  test('should debug DOM structure', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // ページタイトルを確認
    console.log('Page title:', await page.title());
    
    // 全てのボタンを確認
    const buttons = await page.locator('button').all();
    console.log('Total buttons found:', buttons.length);
    
    for (let i = 0; i < Math.min(buttons.length, 10); i++) {
      const buttonText = await buttons[i].textContent();
      console.log(`Button ${i}:`, buttonText);
    }
    
    // h1タグを確認
    const h1Elements = await page.locator('h1').all();
    console.log('H1 elements found:', h1Elements.length);
    
    for (const h1 of h1Elements) {
      const h1Text = await h1.textContent();
      console.log('H1 text:', h1Text);
    }
    
    // サイドバー関連の要素を確認
    const sidebarElements = await page.locator('[class*="sidebar"]').all();
    console.log('Sidebar elements found:', sidebarElements.length);
    
    // プログレスバー関連の要素を確認
    const progressElements = await page.locator('[class*="progress"]').all();
    console.log('Progress elements found:', progressElements.length);
    
    // 全てのクラス名を持つ要素を確認
    const allElements = await page.locator('*[class]').all();
    console.log('Elements with classes found:', allElements.length);
    
    // 最初の20個の要素のクラス名を出力
    for (let i = 0; i < Math.min(allElements.length, 20); i++) {
      const className = await allElements[i].getAttribute('class');
      const tagName = await allElements[i].evaluate(el => el.tagName);
      console.log(`Element ${i}: ${tagName}.${className}`);
    }
    
    // スクリーンショットを撮影
    await page.screenshot({ path: 'debug-dom-structure.png', fullPage: true });
    
    // この「テスト」は実際にはテストではなく、DOM構造を調査するためのもの
    expect(true).toBe(true);
  });
  
  test('should find Marketing Flow Dashboard text', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // 「Marketing Flow Dashboard」というテキストを含む要素を探す
    const titleElements = await page.locator('text=Marketing Flow Dashboard').all();
    console.log('Title elements found:', titleElements.length);
    
    if (titleElements.length > 0) {
      const titleText = await titleElements[0].textContent();
      console.log('Title text found:', titleText);
      
      const titleTag = await titleElements[0].evaluate(el => el.tagName);
      console.log('Title tag:', titleTag);
      
      const titleClass = await titleElements[0].getAttribute('class');
      console.log('Title class:', titleClass);
    }
    
    // プロジェクト管理関連のテキストを探す
    const projectElements = await page.locator('text=プロジェクト管理').all();
    console.log('Project management elements found:', projectElements.length);
    
    expect(titleElements.length).toBeGreaterThan(0);
  });
});