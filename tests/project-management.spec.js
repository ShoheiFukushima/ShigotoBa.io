const { test, expect } = require('@playwright/test');

test.describe('Project Management Flow', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should create a new project successfully', async ({ page }) => {
    // プロジェクト管理エクスパンダーをクリック
    await page.click('text=📂 プロジェクト管理');
    
    // 少し待機してエクスパンダーが開くのを待つ
    await page.waitForTimeout(1000);
    
    // 新規プロジェクト名を入力
    const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
    await expect(projectNameInput).toBeVisible();
    await projectNameInput.fill('テストプロジェクト1');
    
    // 新規作成ボタンをクリック
    await page.click('text=➕ 新規作成');
    
    // 成功メッセージの確認
    const successMessage = page.locator('text=✅ プロジェクト \'テストプロジェクト1\' を作成しました');
    await expect(successMessage).toBeVisible({ timeout: 10000 });
    
    // 現在のプロジェクト情報が表示されているか確認
    const currentProject = page.locator('text=現在のプロジェクト: **テストプロジェクト1**');
    await expect(currentProject).toBeVisible();
  });

  test('should switch between projects', async ({ page }) => {
    // 最初のプロジェクトを作成
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
    await projectNameInput.fill('プロジェクトA');
    await page.click('text=➕ 新規作成');
    
    // 成功メッセージを待つ
    await expect(page.locator('text=✅ プロジェクト \'プロジェクトA\' を作成しました')).toBeVisible({ timeout: 10000 });
    
    // 2番目のプロジェクトを作成
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    await projectNameInput.fill('プロジェクトB');
    await page.click('text=➕ 新規作成');
    
    await expect(page.locator('text=✅ プロジェクト \'プロジェクトB\' を作成しました')).toBeVisible({ timeout: 10000 });
    
    // プロジェクト選択ドロップダウンでプロジェクトAに切り替え
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    const projectSelector = page.locator('select');
    await projectSelector.selectOption('プロジェクトA');
    
    // プロジェクトAが現在のプロジェクトになっているか確認
    const currentProjectA = page.locator('text=現在のプロジェクト: **プロジェクトA**');
    await expect(currentProjectA).toBeVisible({ timeout: 10000 });
  });

  test('should display projects in sidebar stack', async ({ page }) => {
    // プロジェクトを作成
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
    await projectNameInput.fill('サイドバーテスト');
    await page.click('text=➕ 新規作成');
    
    await expect(page.locator('text=✅ プロジェクト \'サイドバーテスト\' を作成しました')).toBeVisible({ timeout: 10000 });
    
    // サイドバーでプロジェクトカードが表示されているか確認
    const projectCard = page.locator('.project-card');
    await expect(projectCard).toBeVisible();
    
    // プロジェクト名がカードに表示されているか確認
    const projectTitle = page.locator('.project-title:has-text("サイドバーテスト")');
    await expect(projectTitle).toBeVisible();
    
    // 進捗情報が表示されているか確認
    const progressInfo = page.locator('text=ステージ 1/8');
    await expect(progressInfo).toBeVisible();
  });

  test('should show project management controls', async ({ page }) => {
    // 複数プロジェクトを作成
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
    
    // プロジェクト1
    await projectNameInput.fill('管理テスト1');
    await page.click('text=➕ 新規作成');
    await expect(page.locator('text=✅ プロジェクト \'管理テスト1\' を作成しました')).toBeVisible({ timeout: 10000 });
    
    // プロジェクト2
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    await projectNameInput.fill('管理テスト2');
    await page.click('text=➕ 新規作成');
    await expect(page.locator('text=✅ プロジェクト \'管理テスト2\' を作成しました')).toBeVisible({ timeout: 10000 });
    
    // 並び替えボタンが表示されているか確認
    const sortButton = page.locator('text=🔀 並び替え');
    await expect(sortButton).toBeVisible();
    
    const createdOrderButton = page.locator('text=📅 作成順');
    await expect(createdOrderButton).toBeVisible();
    
    // 移動ボタンが表示されているか確認
    const upButton = page.locator('button:has-text("⬆️")');
    await expect(upButton).toBeVisible();
    
    const downButton = page.locator('button:has-text("⬇️")');
    await expect(downButton).toBeVisible();
  });
});