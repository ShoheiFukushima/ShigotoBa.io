import { test, expect } from '@playwright/test';

test.describe('サイドバーとヘッダーの動作テスト', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8501');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
  });

  test('ヘッダーが正しく表示される', async ({ page }) => {
    // ヘッダーの存在確認
    const header = await page.locator('.fixed-header');
    await expect(header).toBeVisible();
    
    // ヘッダーの高さが34pxであることを確認
    const headerBox = await header.boundingBox();
    expect(headerBox.height).toBe(34);
    
    // ヘッダーのタイトルが表示されることを確認
    const headerTitle = await header.locator('.header-title');
    await expect(headerTitle).toContainText('SHIGOTOBA.IO');
    
    // フォントサイズが11pxであることを確認
    const fontSize = await headerTitle.evaluate(el => 
      window.getComputedStyle(el).fontSize
    );
    expect(fontSize).toBe('11px');
  });

  test('サイドバーの最小化と展開', async ({ page }) => {
    // サイドバーの初期状態を確認
    const sidebar = await page.locator('section[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    
    // サイドバーを閉じる - Streamlitのトグルボタンを探す
    const toggleButton = await page.locator('[aria-label*="navigation"]').or(page.locator('button').filter({hasText: '×'})).first();
    if (await toggleButton.isVisible()) {
      await toggleButton.click();
      await page.waitForTimeout(500);
      
      // サイドバーが30pxに縮小されることを確認
      const sidebarBox = await sidebar.boundingBox();
      expect(sidebarBox.width).toBe(30);
    }
    
    // サイドバーが閉じた状態でもヘッダーが表示されることを確認
    const header = await page.locator('.fixed-header');
    await expect(header).toBeVisible();
  });

  test('サイドバーのホバー展開機能', async ({ page }) => {
    // サイドバーを閉じる
    const toggleButton = await page.locator('[aria-label*="navigation"]').or(page.locator('button').filter({hasText: '×'})).first();
    if (await toggleButton.isVisible()) {
      await toggleButton.click();
      await page.waitForTimeout(500);
    }
    
    const sidebar = await page.locator('section[data-testid="stSidebar"]');
    
    // サイドバーの右端7ピクセルの位置を計算
    const sidebarBox = await sidebar.boundingBox();
    const hoverX = sidebarBox.x + sidebarBox.width - 3; // 右端から3ピクセル
    const hoverY = sidebarBox.y + sidebarBox.height / 2; // 中央の高さ
    
    // ホバー前の幅を確認
    expect(sidebarBox.width).toBe(30);
    
    // 右端7ピクセルにホバー
    await page.mouse.move(hoverX, hoverY);
    await page.waitForTimeout(500);
    
    // サイドバーが展開されることを確認
    const expandedSidebarBox = await sidebar.boundingBox();
    expect(expandedSidebarBox.width).toBeGreaterThan(250);
  });

  test('プロジェクト選択ドロップダウン', async ({ page }) => {
    // プロジェクト選択ドロップダウンが表示されることを確認 - Streamlitのselectboxを探す
    const projectSelector = await page.locator('[data-testid="stSelectbox"]').first();
    await expect(projectSelector).toBeVisible();
    
    // プロジェクトを選択 - Streamlitの選択方法
    await projectSelector.click();
    await page.waitForTimeout(300);
    const option = await page.locator('[data-testid="stSelectboxOption"]').nth(1);
    if (await option.isVisible()) {
      await option.click();
      await page.waitForTimeout(500);
      
      // 選択したプロジェクトがヘッダーに表示されることを確認
      const headerInfo = await page.locator('.header-info');
      const projectText = await headerInfo.textContent();
      expect(projectText).toContain('ECサイトリニューアル');
    }
  });

  test('アコーディオンメニューの動作', async ({ page }) => {
    // Streamlitのexpander（アコーディオン）を探す
    const expanders = await page.locator('[data-testid="stExpander"]');
    
    // 新規開発メニューを展開
    const devExpander = await expanders.filter({ hasText: '新規開発' }).first();
    if (await devExpander.isVisible()) {
      await devExpander.click();
      await page.waitForTimeout(300);
      
      // メニュー項目が表示されることを確認
      const buttons = await page.locator('[data-testid="stButton"] button');
      await expect(buttons.filter({ hasText: '開発室' })).toBeVisible();
    }
    
    // 運営・分析メニューを展開
    const analysisExpander = await expanders.filter({ hasText: '運営・分析' }).first();
    if (await analysisExpander.isVisible()) {
      await analysisExpander.click();
      await page.waitForTimeout(300);
      
      // メニュー項目が表示されることを確認
      await expect(buttons.filter({ hasText: 'パフォーマンスダッシュボード' })).toBeVisible();
    }
  });

  test('ページ遷移時のヘッダー永続性', async ({ page }) => {
    // 開発室に遷移 - Streamlitのexpanderとボタンを使用
    const expanders = await page.locator('[data-testid="stExpander"]');
    const devExpander = await expanders.filter({ hasText: '新規開発' }).first();
    
    if (await devExpander.isVisible()) {
      await devExpander.click();
      await page.waitForTimeout(300);
      
      const devRoomButton = await page.locator('[data-testid="stButton"] button').filter({ hasText: '開発室' });
      if (await devRoomButton.isVisible()) {
        await devRoomButton.click();
        await page.waitForLoadState('networkidle');
        
        // ヘッダーが引き続き表示されることを確認
        const header = await page.locator('.fixed-header');
        await expect(header).toBeVisible();
        
        // ヘッダーの高さが維持されることを確認
        const headerBox = await header.boundingBox();
        expect(headerBox.height).toBe(34);
      }
    }
  });

  test('レイヤー順序の確認', async ({ page }) => {
    // ヘッダーのz-indexを確認
    const headerZIndex = await page.locator('.fixed-header').evaluate(el => 
      window.getComputedStyle(el).zIndex
    );
    expect(parseInt(headerZIndex)).toBe(10000);
    
    // サイドバーのz-indexを確認
    const sidebarZIndex = await page.locator('section[data-testid="stSidebar"]').evaluate(el => 
      window.getComputedStyle(el).zIndex
    );
    expect(parseInt(sidebarZIndex)).toBe(9999);
    
    // ヘッダーがサイドバーより上位にあることを確認
    expect(parseInt(headerZIndex)).toBeGreaterThan(parseInt(sidebarZIndex));
  });

  test('サイドバー最小化時の境界線表示', async ({ page }) => {
    // サイドバーを閉じる
    const toggleButton = await page.locator('[aria-label*="navigation"]').or(page.locator('button').filter({hasText: '×'})).first();
    if (await toggleButton.isVisible()) {
      await toggleButton.click();
      await page.waitForTimeout(500);
    }
    
    // 境界線が表示されることを確認
    const sidebar = await page.locator('section[data-testid="stSidebar"]');
    const borderRight = await sidebar.evaluate(el => 
      window.getComputedStyle(el).borderRight
    );
    expect(borderRight).toContain('1px solid');
  });
});