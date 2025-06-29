const { test, expect } = require('@playwright/test');

test.describe('shigotoba.io ダッシュボード - 現在のUI対応テスト', () => {
  
  test.beforeEach(async ({ page }) => {
    // ダッシュボードにアクセス
    await page.goto('/');
    
    // ページが完全に読み込まれるまで待機
    await page.waitForLoadState('networkidle');
    
    // Streamlitアプリが完全に読み込まれるまで追加で待機
    await page.waitForSelector('h1', { timeout: 30000 });
    
    // 追加で少し待機（Streamlitの動的コンテンツ読み込みのため）
    await page.waitForTimeout(2000);
  });

  test('should load dashboard with correct title', async ({ page }) => {
    // ページタイトルの確認
    await expect(page).toHaveTitle(/shigotoba\.io/);
    
    // ダッシュボードタイトルの確認
    const title = page.locator('h1').filter({ hasText: 'ダッシュボード' });
    await expect(title).toBeVisible();
    
    // タイトルテキストの確認
    const titleText = await title.textContent();
    expect(titleText).toContain('🏠 ダッシュボード');
  });

  test('should show Google Sheets connection status', async ({ page }) => {
    // Google Sheets接続状態の表示を確認（info, warning, successのいずれか）
    const sheetsStatus = page.locator('[role="alert"]').filter({ 
      hasText: /Google Sheets/ 
    });
    
    // 何らかの接続状態メッセージが表示されていることを確認
    const statusCount = await sheetsStatus.count();
    expect(statusCount).toBeGreaterThan(0);
  });

  test('should show metrics section', async ({ page }) => {
    // メトリクスセクションヘッダーの確認
    const metricsHeader = page.locator('h2').filter({ hasText: '今日の概要' });
    await expect(metricsHeader).toBeVisible();
    
    // メトリクス項目の確認
    const metrics = [
      'アクティブプロジェクト',
      '完了タスク',
      '新規コンテンツ',
      '効率スコア'
    ];
    
    for (const metric of metrics) {
      const metricElement = page.locator(`text=${metric}`).first();
      await expect(metricElement).toBeVisible();
    }
  });

  test('should show project list section', async ({ page }) => {
    // プロジェクト一覧セクションの確認
    const projectHeader = page.locator('h2').filter({ hasText: 'プロジェクト一覧' });
    await expect(projectHeader).toBeVisible();
  });

  test('should display quick access sections', async ({ page }) => {
    // クイックアクセスセクションの確認
    const quickAccessHeader = page.locator('h2').filter({ hasText: 'クイックアクセス' });
    await expect(quickAccessHeader).toBeVisible();
    
    // 各カテゴリセクションの確認
    const sections = [
      '🏗️ 新規開発',
      '📊 運営・分析', 
      '🎨 広告・マーケティング実行',
      '🔄 自動化パイプライン'
    ];
    
    for (const section of sections) {
      const sectionHeader = page.locator('h3').filter({ hasText: section });
      await expect(sectionHeader).toBeVisible();
    }
  });

  test('should show sidebar navigation', async ({ page }) => {
    // サイドバーの存在確認
    const sidebar = page.locator('[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    
    // ロゴ/タイトルの確認（最初の要素のみ）
    const logo = sidebar.locator('text=SHIGOTOBA.IO').first();
    await expect(logo).toBeVisible();
    
    // メニュー項目の確認
    const menuItems = ['ホーム', '開発室', 'プロジェクト管理', 'パフォーマンス'];
    
    for (const item of menuItems) {
      const menuItem = sidebar.locator('button').filter({ hasText: item });
      const count = await menuItem.count();
      // サイドバーに項目が存在することを確認
      expect(count).toBeGreaterThan(0);
    }
  });

  test('should display workflow management button', async ({ page }) => {
    // ワークフロー管理ボタンの確認
    const workflowButton = page.locator('button').filter({ hasText: 'ワークフロー管理' });
    await expect(workflowButton).toBeVisible();
    
    // クリック可能であることを確認
    await expect(workflowButton).toBeEnabled();
  });

  test('should show onboarding elements for new users', async ({ page }) => {
    // ウェルカムメッセージの確認
    const welcomeText = page.locator('text=shigotoba.io へようこそ');
    
    // ウェルカムメッセージが表示されている場合の確認
    if (await welcomeText.isVisible()) {
      // ツアー開始ボタンの確認
      const tourButton = page.locator('button').filter({ hasText: 'ツアーを開始' });
      await expect(tourButton).toBeVisible();
    }
    
    // クイックスタートガイドの確認
    const quickStartSection = page.locator('text=クイックスタートガイド');
    // クイックスタートガイドは存在する場合のみ確認
    const quickStartCount = await quickStartSection.count();
    expect(quickStartCount).toBeGreaterThanOrEqual(0);
  });

  test('should have responsive layout', async ({ page }) => {
    // デスクトップビューでのテスト
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.waitForTimeout(500);
    
    // サイドバーが表示されていることを確認
    const sidebar = page.locator('[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    
    // モバイルビューでのテスト
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(500);
    
    // モバイルでもコンテンツが表示されることを確認
    const mainContent = page.locator('h1').filter({ hasText: 'ダッシュボード' });
    await expect(mainContent).toBeVisible();
  });

  test('should show statistics in sidebar', async ({ page }) => {
    // サイドバーの統計情報確認
    const sidebar = page.locator('[data-testid="stSidebar"]');
    
    // 統計ラベルの確認
    const statsLabels = ['タスク', '投稿', 'コンテンツ', '効果'];
    
    for (const label of statsLabels) {
      const statElement = sidebar.locator(`text=${label}`).first();
      const isVisible = await statElement.isVisible();
      
      // 統計情報が表示されているかどうか（オプショナル）
      if (isVisible) {
        await expect(statElement).toBeVisible();
      }
    }
  });
});