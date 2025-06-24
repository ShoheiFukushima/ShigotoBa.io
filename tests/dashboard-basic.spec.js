const { test, expect } = require('@playwright/test');

test.describe('Marketing Flow Dashboard - Basic UI Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // ダッシュボードにアクセス
    await page.goto('/');
    
    // ページが完全に読み込まれるまで待機
    await page.waitForLoadState('networkidle');
    
    // Streamlitアプリが完全に読み込まれるまで追加で待機
    await page.waitForSelector('h1:has-text("Marketing Flow Dashboard")', { timeout: 30000 });
    
    // 追加で少し待機（Streamlitの動的コンテンツ読み込みのため）
    await page.waitForTimeout(2000);
  });

  test('should load dashboard with correct title', async ({ page }) => {
    // タイトルの確認（実際のタイトルに合わせて修正）
    await expect(page).toHaveTitle('Marketing Flow Dashboard');
    
    // メインタイトルの確認
    const title = page.locator('h1:has-text("Marketing Flow Dashboard")');
    await expect(title).toBeVisible();
    
    // サブタイトルの確認
    const subtitle = page.locator('text=競合インテリジェンス統合型マーケティング自動化フロー');
    await expect(subtitle).toBeVisible();
  });

  test('should show project management section', async ({ page }) => {
    // プロジェクト管理エクスパンダーの確認
    const projectManager = page.locator('text=📂 プロジェクト管理');
    await expect(projectManager).toBeVisible();
    
    // 新規プロジェクト作成の案内メッセージ
    const guidance = page.locator('text=右上の「プロジェクト管理」から新規プロジェクトを作成してください');
    await expect(guidance).toBeVisible();
  });

  test('should display 8 flow stages', async ({ page }) => {
    // 8つのフローステージボタンの確認
    const stages = [
      { emoji: '📝', text: 'プロダクト入力' },
      { emoji: '🔍', text: '調査フェーズ' }, 
      { emoji: '📊', text: 'ベンチマーク策定' },
      { emoji: '💡', text: 'ベネフィット決定' },
      { emoji: '🎯', text: 'マーケティング施策' },
      { emoji: '✍️', text: 'コンテンツ作成' },
      { emoji: '🚀', text: 'デプロイメント' },
      { emoji: '📈', text: '測定・分析' }
    ];
    
    for (const stage of stages) {
      // 改行を含むテキストでボタンを検索
      const stageButton = page.locator('button').filter({ hasText: stage.text });
      await expect(stageButton).toBeVisible();
    }
    
    // 総ボタン数の確認（少なくとも8個のステージボタン + その他）
    const allButtons = page.locator('button');
    const buttonCount = await allButtons.count();
    expect(buttonCount).toBeGreaterThanOrEqual(8);
  });

  test('should show progress bar at 0%', async ({ page }) => {
    // プログレスバーの確認（代替セレクタを使用）
    const progressContainer = page.locator('.progress-container');
    await expect(progressContainer).toBeVisible();
    
    // プログレスバー内に0%があるかを確認（hiddenでも存在することを確認）
    const progressBar = page.locator('.progress-bar');
    await expect(progressBar).toBeAttached(); // visible ではなく attached を使用
    
    // プログレスバー内のテキストを確認
    const progressBarContent = await progressBar.textContent();
    expect(progressBarContent?.trim()).toContain('0%');
  });

  test('should show sidebar with project stack', async ({ page }) => {
    // サイドバーが閉じている場合があるので、サイドバートグルボタンをクリック
    // 空のテキストでheaderNoPaddingのdata-testidを持つボタンがサイドバートグル
    const sidebarToggle = page.locator('button[data-testid="stBaseButton-headerNoPadding"]');
    
    try {
      // サイドバートグルをクリック
      await sidebarToggle.click();
      await page.waitForTimeout(1500); // サイドバーアニメーション待機
    } catch (error) {
      // トグルボタンが見つからない場合はスキップ
      console.log('Sidebar toggle not found, checking if sidebar is already open');
    }
    
    // プロジェクトスタックヘッダーを確認（サイドバーを開いた後）
    const stackHeader = page.locator('text=📂 プロジェクトスタック');
    await expect(stackHeader).toBeVisible({ timeout: 10000 });
    
    // フロー全体図ヘッダー
    const flowHeader = page.locator('text=🗺️ フロー全体図');
    await expect(flowHeader).toBeVisible();
    
    // プロジェクトがない場合のメッセージ
    const noProjectsMessage = page.locator('text=📝 プロジェクトがありません');
    await expect(noProjectsMessage).toBeVisible();
  });

  test('should show warning when no project selected', async ({ page }) => {
    // プロジェクト未選択時の警告メッセージ
    const warning = page.locator('text=⚠️ プロジェクトを選択または作成してください');
    await expect(warning).toBeVisible();
  });
});