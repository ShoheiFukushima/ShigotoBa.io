const { test, expect } = require('@playwright/test');

test.describe('Marketing Flow Dashboard - Basic UI Tests', () => {
  
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
    // タイトルの確認（実際のタイトルに合わせて修正）
    await expect(page).toHaveTitle('shigotoba.io - マーケティング自動化');
    
    // メインタイトルの確認（現在のUIに合わせて修正）
    const title = page.locator('h1');
    await expect(title).toBeVisible();
    
    // ダッシュボードタイトルの内容を確認
    const titleText = await title.textContent();
    expect(titleText).toMatch(/(🏠 ダッシュボード|おはようございます|こんにちは|こんばんは)/);
  });

  test('should show project management section', async ({ page }) => {
    // プロジェクト管理室ボタンの確認（より具体的なテキストで検索）
    const projectManagerButton = page.locator('button').filter({ hasText: '管理室' });
    await expect(projectManagerButton).toBeVisible();
    
    // サイドバーのクイックアクションの確認
    const newProjectButton = page.locator('button').filter({ hasText: '新規プロジェクト' });
    await expect(newProjectButton).toBeVisible();
  });

  test('should display main category buttons', async ({ page }) => {
    // メインカテゴリボタンの確認（重複を避けるため、より具体的な検索）
    const categories = [
      '📋 開発室',  // 具体的な絵文字付きテキストで検索
      'プロダクト',
      'A/Bテスト', 
      'パフォーマンス',
      'AI Creative',
      'リアルタイム',
      'マニュアル',
      '設定'
    ];
    
    for (const category of categories) {
      // 各カテゴリのボタンを検索（first()で最初の要素を選択）
      const categoryButton = page.locator('button').filter({ hasText: category }).first();
      await expect(categoryButton).toBeVisible();
    }
    
    // 総ボタン数の確認（少なくとも8個以上）
    const allButtons = page.locator('button');
    const buttonCount = await allButtons.count();
    expect(buttonCount).toBeGreaterThanOrEqual(8);
  });

  test('should show metrics cards', async ({ page }) => {
    // メトリクスカードの確認
    const metricsElements = [
      'アクティブプロジェクト',
      '未完了タスク',
      '今週の成果',
      '効率スコア'
    ];
    
    for (const metric of metricsElements) {
      // 各メトリクスの存在を確認
      const metricElement = page.locator(`text=${metric}`);
      await expect(metricElement).toBeVisible();
    }
  });

  test('should show sidebar with quick actions', async ({ page }) => {
    // サイドバーのクイックアクションヘッダーを確認
    const quickActionsHeader = page.locator('text=⚡ クイックアクション');
    await expect(quickActionsHeader).toBeVisible();
    
    // 統計セクション
    const statsHeader = page.locator('text=📊 今週の統計');
    await expect(statsHeader).toBeVisible();
    
    // 通知セクション
    const notificationsHeader = page.locator('text=🔔 通知');
    await expect(notificationsHeader).toBeVisible();
    
    // サイドバーの統計データ確認（最初の要素のみ）
    const completedTasks = page.locator('text=完了タスク').first();
    await expect(completedTasks).toBeVisible();
  });

  test('should show document archive section', async ({ page }) => {
    // ドキュメント書庫セクションの確認
    const documentHeader = page.locator('text=📚 ドキュメント書庫');
    await expect(documentHeader).toBeVisible();
    
    // ドキュメントカテゴリの確認
    const manualCategory = page.locator('text=マニュアル・ガイド');
    await expect(manualCategory).toBeVisible();
    
    const reportCategory = page.locator('text=レポート・分析');
    await expect(reportCategory).toBeVisible();
  });
});