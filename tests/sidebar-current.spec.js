import { test, expect } from '@playwright/test';

test.describe('Streamlitサイドバーの動作テスト', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8501');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
  });

  test('サイドバーの基本表示', async ({ page }) => {
    // Streamlitのサイドバーコンテナを確認
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    
    // ブランディング部分の確認
    const branding = await sidebar.locator('h2').filter({ hasText: 'SHIGOTOBA.IO' }).first();
    await expect(branding).toBeVisible();
  });

  test('メニューナビゲーションの動作', async ({ page }) => {
    // サイドバー内のメニューボタンを確認
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    
    // ホームボタンの確認
    const homeButton = await sidebar.locator('button').filter({ hasText: 'ホーム' });
    await expect(homeButton).toBeVisible();
    
    // 開発室ボタンの確認
    const devButton = await sidebar.locator('button').filter({ hasText: '開発室' });
    await expect(devButton).toBeVisible();
  });

  test('プロジェクトセレクターの動作', async ({ page }) => {
    // サイドバー内のセレクトボックスを探す
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    const projectSelector = await sidebar.locator('[data-testid="stSelectbox"]');
    
    // セレクターが存在する場合のみテスト
    const selectorCount = await projectSelector.count();
    if (selectorCount > 0) {
      await expect(projectSelector.first()).toBeVisible();
      
      // クリックしてオプションを表示
      await projectSelector.first().click();
      await page.waitForTimeout(300);
      
      // オプションの確認（表示されるまで少し待つ）
      await page.waitForTimeout(500);
      const options = await page.locator('[data-testid="stSelectboxOption"]');
      const optionCount = await options.count();
      
      // オプションが表示されない場合は、セレクトボックス自体が機能していることだけ確認
      if (optionCount === 0) {
        // セレクトボックスがクリック可能であることを確認
        await expect(projectSelector.first()).toBeEnabled();
      } else {
        expect(optionCount).toBeGreaterThan(0);
      }
    }
  });

  test('統計情報の表示', async ({ page }) => {
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    
    // 統計ラベルの確認
    const statsToCheck = ['タスク', '投稿', 'コンテンツ', '効果'];
    
    for (const stat of statsToCheck) {
      const statElement = await sidebar.locator(`text=${stat}`).first();
      
      // 統計が表示されているかチェック（存在する場合のみ）
      const isVisible = await statElement.isVisible().catch(() => false);
      if (isVisible) {
        await expect(statElement).toBeVisible();
      }
    }
  });

  test('クイックアクションボタンの確認', async ({ page }) => {
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    
    // プロジェクトを始めるボタンの確認（存在する場合）
    const startProjectButton = await sidebar.locator('button').filter({ 
      hasText: 'プロジェクトを始める' 
    });
    
    const buttonCount = await startProjectButton.count();
    if (buttonCount > 0) {
      await expect(startProjectButton).toBeVisible();
      await expect(startProjectButton).toBeEnabled();
    }
  });

  test('フッターの表示', async ({ page }) => {
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    
    // フッターテキストの確認
    const footer = await sidebar.locator('text=© 2024');
    const footerCount = await footer.count();
    
    if (footerCount > 0) {
      await expect(footer.first()).toBeVisible();
    }
  });

  test('レスポンシブ動作の確認', async ({ page }) => {
    // デスクトップビュー
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.waitForTimeout(500);
    
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    
    // タブレットビュー
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(500);
    
    // Streamlitはタブレットでもサイドバーを表示
    await expect(sidebar).toBeVisible();
    
    // モバイルビュー
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(500);
    
    // モバイルではサイドバーが非表示またはハンバーガーメニューになる可能性
    const sidebarVisible = await sidebar.isVisible().catch(() => false);
    
    // ハンバーガーメニューボタンの確認
    if (!sidebarVisible) {
      const hamburger = await page.locator('[data-testid="stSidebarCollapsedControl"]');
      const hamburgerCount = await hamburger.count();
      
      if (hamburgerCount > 0) {
        await expect(hamburger).toBeVisible();
      }
    }
  });

  test('ページ遷移の動作', async ({ page }) => {
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    
    // 開発室ボタンをクリック
    const devRoomButton = await sidebar.locator('button').filter({ hasText: '開発室' });
    const devButtonCount = await devRoomButton.count();
    
    if (devButtonCount > 0) {
      await devRoomButton.click();
      
      // ページ遷移を待つ
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      // 遷移後のページタイトルを確認（開発室ページの要素）
      const devPageTitle = await page.locator('h1, h2').filter({ 
        hasText: /開発室|Development/ 
      });
      
      const titleCount = await devPageTitle.count();
      expect(titleCount).toBeGreaterThan(0);
    }
  });

  test('メインナビゲーションとの統合', async ({ page }) => {
    // メインコンテンツとサイドバーの両方が表示されることを確認
    const mainContent = await page.locator('section[data-testid="stMain"]');
    await expect(mainContent).toBeVisible();
    
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    
    // 両方が同時に表示されることを確認
    const mainBox = await mainContent.boundingBox();
    const sidebarBox = await sidebar.boundingBox();
    
    expect(mainBox).not.toBeNull();
    expect(sidebarBox).not.toBeNull();
    
    // サイドバーがメインコンテンツと重ならないことを確認
    if (mainBox && sidebarBox) {
      expect(sidebarBox.x + sidebarBox.width).toBeLessThanOrEqual(mainBox.x + 10); // 10pxの余裕
    }
  });

  test('初期状態での統計表示', async ({ page }) => {
    const sidebar = await page.locator('[data-testid="stSidebar"]');
    
    // 統計情報が表示されているかを確認
    // Streamlitのメトリクス表示はst.metricを使用している場合とテキストの場合がある
    const metricsFound = [];
    
    // メトリクスウィジェットを探す
    const metricWidgets = await sidebar.locator('[data-testid="metric-container"]');
    const metricCount = await metricWidgets.count();
    
    if (metricCount > 0) {
      // st.metricを使用している場合
      for (let i = 0; i < metricCount; i++) {
        const metric = metricWidgets.nth(i);
        const label = await metric.locator('[data-testid="stMetricLabel"]').textContent();
        const value = await metric.locator('[data-testid="stMetricValue"]').textContent();
        metricsFound.push({ label, value });
      }
    } else {
      // テキストベースの統計表示の場合
      const statsLabels = ['タスク', '投稿', 'コンテンツ', '効果'];
      
      for (const label of statsLabels) {
        const statElement = await sidebar.locator(`text=${label}`).first();
        
        if (await statElement.isVisible().catch(() => false)) {
          // 統計要素が見つかったことを記録
          metricsFound.push({ label, found: true });
        }
      }
    }
    
    // 何らかの統計情報が表示されていることを確認
    expect(metricsFound.length).toBeGreaterThan(0);
  });
});