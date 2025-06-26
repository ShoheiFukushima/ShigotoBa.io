import { test, expect } from '@playwright/test';

test.describe('強化版サイドバーの動作テスト', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8501');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
  });

  test('強化版サイドバーの基本表示', async ({ page }) => {
    // カスタムHTMLコンポーネントの確認
    const sidebarContainer = await page.locator('#sidebarContainer');
    await expect(sidebarContainer).toBeVisible();
    
    // 初期状態でexpandedクラスを持つことを確認
    const isExpanded = await sidebarContainer.evaluate(el => 
      el.classList.contains('expanded')
    );
    expect(isExpanded).toBe(true);
  });

  test('トグルボタンでの最小化/展開', async ({ page }) => {
    // トグルボタンを探す
    const toggleButton = await page.locator('.sidebar-toggle');
    await expect(toggleButton).toBeVisible();
    
    // クリックして最小化
    await toggleButton.click();
    await page.waitForTimeout(500);
    
    // collapsedクラスが追加されることを確認
    const sidebarContainer = await page.locator('#sidebarContainer');
    const isCollapsed = await sidebarContainer.evaluate(el => 
      el.classList.contains('collapsed')
    );
    expect(isCollapsed).toBe(true);
    
    // 幅が30pxになることを確認
    const width = await sidebarContainer.evaluate(el => 
      window.getComputedStyle(el).width
    );
    expect(width).toBe('30px');
  });

  test('ホバーゾーンでの展開', async ({ page }) => {
    // まず最小化
    const toggleButton = await page.locator('.sidebar-toggle');
    await toggleButton.click();
    await page.waitForTimeout(500);
    
    // ホバーゾーンを探す
    const hoverZone = await page.locator('.hover-zone');
    await expect(hoverZone).toBeVisible();
    
    // ホバーゾーンにマウスを移動
    await hoverZone.hover();
    await page.waitForTimeout(500);
    
    // サイドバーが展開されることを確認
    const sidebarContainer = await page.locator('#sidebarContainer');
    const isExpanded = await sidebarContainer.evaluate(el => 
      el.classList.contains('expanded')
    );
    expect(isExpanded).toBe(true);
  });

  test('アコーディオンメニューの動作', async ({ page }) => {
    // 開発メニューのヘッダーをクリック
    const devHeader = await page.locator('.accordion-header').filter({ hasText: '新規開発' });
    await devHeader.click();
    await page.waitForTimeout(300);
    
    // activeクラスが追加されることを確認
    const isActive = await devHeader.evaluate(el => 
      el.classList.contains('active')
    );
    expect(isActive).toBe(true);
    
    // コンテンツが展開されることを確認
    const devContent = await page.locator('#dev');
    const isContentActive = await devContent.evaluate(el => 
      el.classList.contains('active')
    );
    expect(isContentActive).toBe(true);
    
    // メニュー項目が表示されることを確認
    const menuItem = await page.locator('.menu-item').filter({ hasText: '開発室' });
    await expect(menuItem).toBeVisible();
  });

  test('プロジェクト選択の動作', async ({ page }) => {
    // Streamlitのselectboxを探す
    const projectSelector = await page.locator('[data-testid="stSelectbox"]').first();
    await expect(projectSelector).toBeVisible();
    
    // プロジェクトを選択
    await projectSelector.click();
    await page.waitForTimeout(300);
    
    const option = await page.locator('[data-testid="stSelectboxOption"]').filter({ hasText: 'ECサイトリニューアル' });
    if (await option.isVisible()) {
      await option.click();
      await page.waitForTimeout(500);
      
      // 選択が反映されることを確認
      const selectedText = await projectSelector.textContent();
      expect(selectedText).toContain('ECサイトリニューアル');
    }
  });

  test('ページ遷移の動作', async ({ page }) => {
    // 開発メニューを展開
    const devHeader = await page.locator('.accordion-header').filter({ hasText: '新規開発' });
    await devHeader.click();
    await page.waitForTimeout(300);
    
    // 開発室リンクをクリック
    const devRoomLink = await page.locator('.menu-item').filter({ hasText: '開発室' });
    await devRoomLink.click();
    
    // URLが変更されることを確認（Streamlitの場合、ページ全体がリロードされる）
    await page.waitForLoadState('networkidle');
    
    // ページタイトルまたは特定の要素で遷移を確認
    const pageTitle = await page.title();
    expect(pageTitle).toContain('開発室');
  });

  test('レスポンシブ動作の確認', async ({ page }) => {
    // モバイルビューポートに変更
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(500);
    
    // 最小化状態で幅が0になることを確認
    const toggleButton = await page.locator('.sidebar-toggle');
    await toggleButton.click();
    await page.waitForTimeout(500);
    
    const sidebarContainer = await page.locator('#sidebarContainer');
    const width = await sidebarContainer.evaluate(el => 
      window.getComputedStyle(el).width
    );
    expect(width).toBe('0px');
    
    // ホバーゾーンの幅が20pxになることを確認
    const hoverZone = await page.locator('.hover-zone');
    const hoverZoneWidth = await hoverZone.evaluate(el => 
      window.getComputedStyle(el).width
    );
    expect(hoverZoneWidth).toBe('20px');
  });

  test('複数アコーディオンの排他制御', async ({ page }) => {
    // 開発メニューを展開
    const devHeader = await page.locator('.accordion-header').filter({ hasText: '新規開発' });
    await devHeader.click();
    await page.waitForTimeout(300);
    
    // 分析メニューを展開
    const analysisHeader = await page.locator('.accordion-header').filter({ hasText: '運営・分析' });
    await analysisHeader.click();
    await page.waitForTimeout(300);
    
    // 開発メニューが閉じられることを確認
    const devContent = await page.locator('#dev');
    const isDevActive = await devContent.evaluate(el => 
      el.classList.contains('active')
    );
    expect(isDevActive).toBe(false);
    
    // 分析メニューが開いていることを確認
    const analysisContent = await page.locator('#analysis');
    const isAnalysisActive = await analysisContent.evaluate(el => 
      el.classList.contains('active')
    );
    expect(isAnalysisActive).toBe(true);
  });

  test('スタイルとアニメーションの確認', async ({ page }) => {
    const sidebarContainer = await page.locator('#sidebarContainer');
    
    // トランジションが設定されていることを確認
    const transition = await sidebarContainer.evaluate(el => 
      window.getComputedStyle(el).transition
    );
    expect(transition).toContain('width');
    expect(transition).toContain('0.3s');
    
    // z-indexが正しく設定されていることを確認
    const zIndex = await sidebarContainer.evaluate(el => 
      window.getComputedStyle(el).zIndex
    );
    expect(parseInt(zIndex)).toBe(9999);
  });
});