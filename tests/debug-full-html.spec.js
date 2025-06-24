const { test, expect } = require('@playwright/test');
const fs = require('fs');

test.describe('Full HTML Debug', () => {
  
  test('should dump full HTML and check Streamlit execution', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('h1:has-text("Marketing Flow Dashboard")', { timeout: 30000 });
    await page.waitForTimeout(5000); // 長めに待機
    
    console.log('=== Full page analysis ===');
    
    // 完全なHTMLをファイルに保存
    const htmlContent = await page.content();
    fs.writeFileSync('debug-full-page.html', htmlContent);
    console.log(`Full HTML saved to debug-full-page.html (${htmlContent.length} chars)`);
    
    // サイドバー関連の検索
    const sidebarMatches = htmlContent.match(/sidebar|プロジェクトスタック|フロー全体図/gi) || [];
    console.log(`HTML contains sidebar-related text: ${sidebarMatches.length} matches`);
    sidebarMatches.forEach((match, i) => console.log(`  ${i}: ${match}`));
    
    // st.sidebar() が実行されているかチェック
    const streamlitSidebarTags = htmlContent.match(/data-testid="[^"]*sidebar[^"]*"/gi) || [];
    console.log(`Streamlit sidebar data-testids: ${streamlitSidebarTags.length}`);
    streamlitSidebarTags.forEach((tag, i) => console.log(`  ${i}: ${tag}`));
    
    // CSS内でsidebarを探す
    const cssMatches = htmlContent.match(/<style[^>]*>([^<]*sidebar[^<]*)<\/style>/gi) || [];
    console.log(`CSS with sidebar: ${cssMatches.length}`);
    
    // JavaScript内でsidebarを探す
    const jsMatches = htmlContent.match(/<script[^>]*>([^<]*sidebar[^<]*)<\/script>/gi) || [];
    console.log(`JavaScript with sidebar: ${jsMatches.length}`);
    
    // Streamlitのレンダリング状態をチェック
    const streamlitElements = await page.locator('[data-testid*="st"]').all();
    console.log(`Total Streamlit elements: ${streamlitElements.length}`);
    
    // 具体的にst要素の一覧を取得
    const stElementsInfo = await page.evaluate(() => {
      const elements = Array.from(document.querySelectorAll('[data-testid*="st"]'));
      return elements.map(el => ({
        testId: el.getAttribute('data-testid'),
        tag: el.tagName,
        visible: el.offsetParent !== null,
        hasText: el.textContent?.trim().length > 0
      })).slice(0, 20); // 上位20個
    });
    
    console.log('=== Streamlit elements (first 20) ===');
    stElementsInfo.forEach((el, i) => {
      console.log(`${i}: ${el.tag}[data-testid="${el.testId}"] visible=${el.visible} hasText=${el.hasText}`);
    });
    
    // with st.sidebar ブロックが実行されたかの痕跡を探す
    const potentialSidebarContent = await page.evaluate(() => {
      // 'プロジェクト'を含む全ての要素を探す
      const elements = Array.from(document.querySelectorAll('*'));
      return elements
        .filter(el => el.textContent && el.textContent.includes('プロジェクト'))
        .map(el => ({
          tag: el.tagName,
          text: el.textContent.trim().substring(0, 100),
          className: el.className,
          visible: el.offsetParent !== null
        }))
        .slice(0, 10);
    });
    
    console.log('=== Elements containing プロジェクト ===');
    potentialSidebarContent.forEach((el, i) => {
      console.log(`${i}: ${el.tag}.${el.className} "${el.text}" visible=${el.visible}`);
    });
    
    // スクリーンショット
    await page.screenshot({ path: 'debug-full-analysis.png', fullPage: true });
    
    expect(true).toBe(true);
  });
});