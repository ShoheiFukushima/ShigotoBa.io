const { test, expect } = require('@playwright/test');

test.describe('Visual Regression Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should match dashboard initial state screenshot', async ({ page }) => {
    // 初期状態のスクリーンショット
    await expect(page).toHaveScreenshot('dashboard-initial.png', {
      fullPage: true,
      threshold: 0.3
    });
  });

  test('should match project creation form', async ({ page }) => {
    // プロジェクト管理フォームを開く
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    // フォーム部分のスクリーンショット
    const projectForm = page.locator('[data-testid="stExpander"]').first();
    await expect(projectForm).toHaveScreenshot('project-creation-form.png');
  });

  test('should match project with data filled', async ({ page }) => {
    // プロジェクト作成
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
    await projectNameInput.fill('ビジュアルテストプロジェクト');
    await page.click('text=➕ 新規作成');
    
    await expect(page.locator('text=✅ プロジェクト \'ビジュアルテストプロジェクト\' を作成しました')).toBeVisible({ timeout: 10000 });
    
    // プロダクト情報入力
    await page.locator('input[placeholder*="AI News Curator"]').fill('ビジュアルテストAI');
    await page.locator('select').first().selectOption('ビジネスツール');
    await page.locator('input[placeholder*="ビジネスパーソン"]').fill('マーケター');
    await page.locator('input[placeholder*="月額980円"]').fill('月額2980円');
    await page.locator('textarea[placeholder*="競合にない強み"]').fill('革新的なAI分析機能とリアルタイム競合追跡');
    
    // フォーム入力後のスクリーンショット
    await expect(page).toHaveScreenshot('dashboard-with-project-data.png', {
      fullPage: true,
      threshold: 0.3
    });
  });

  test('should match flow progression visual state', async ({ page }) => {
    // プロジェクト作成と進行
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
    await projectNameInput.fill('フロー進行テスト');
    await page.click('text=➕ 新規作成');
    
    await expect(page.locator('text=✅ プロジェクト \'フロー進行テスト\' を作成しました')).toBeVisible({ timeout: 10000 });
    
    // Stage 0から1への進行
    await page.locator('input[placeholder*="AI News Curator"]').fill('フロー進行AI');
    await page.locator('select').first().selectOption('情報収集・配信');
    await page.locator('text=次へ: 調査開始 →').click();
    
    // Stage 1のスクリーンショット
    await expect(page.locator('text=🔍 調査フェーズ開始')).toBeVisible({ timeout: 10000 });
    await expect(page).toHaveScreenshot('flow-stage-1-research.png', {
      fullPage: true,
      threshold: 0.3
    });
    
    // Stage 2への進行
    await page.locator('text=次へ: ベンチマーク策定 →').click();
    await expect(page.locator('text=📊 品質ベンチマーク策定')).toBeVisible({ timeout: 10000 });
    
    // Stage 2のスクリーンショット
    await expect(page).toHaveScreenshot('flow-stage-2-benchmark.png', {
      fullPage: true,
      threshold: 0.3
    });
  });

  test('should match sidebar project stack visual', async ({ page }) => {
    // 複数プロジェクト作成
    const projectNames = ['プロジェクトA', 'プロジェクトB', 'プロジェクトC'];
    
    for (const name of projectNames) {
      await page.click('text=📂 プロジェクト管理');
      await page.waitForTimeout(1000);
      
      const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
      await projectNameInput.fill(name);
      await page.click('text=➕ 新規作成');
      
      await expect(page.locator(`text=✅ プロジェクト '${name}' を作成しました`)).toBeVisible({ timeout: 10000 });
    }
    
    // サイドバーのスクリーンショット
    const sidebar = page.locator('[data-testid="stSidebar"]');
    await expect(sidebar).toHaveScreenshot('sidebar-project-stack.png');
  });

  test('should match responsive design on mobile', async ({ page }) => {
    // モバイルビューポートに設定
    await page.setViewportSize({ width: 375, height: 667 });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // モバイル表示のスクリーンショット
    await expect(page).toHaveScreenshot('dashboard-mobile.png', {
      fullPage: true,
      threshold: 0.3
    });
  });

  test('should match dark mode styling', async ({ page }) => {
    // ダークモードのスタイリングが適用されているか確認
    const appContainer = page.locator('.stApp');
    await expect(appContainer).toHaveCSS('background-color', 'rgb(14, 17, 23)');
    
    // プロジェクトカードのスタイリング確認
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
    await projectNameInput.fill('ダークモードテスト');
    await page.click('text=➕ 新規作成');
    
    await expect(page.locator('text=✅ プロジェクト \'ダークモードテスト\' を作成しました')).toBeVisible({ timeout: 10000 });
    
    // プロジェクトカードのスタイルが適用されているか
    const projectCard = page.locator('.project-card');
    await expect(projectCard).toBeVisible();
    
    // 全体のダークモードスタイルスクリーンショット
    await expect(page).toHaveScreenshot('dashboard-dark-mode.png', {
      fullPage: true,
      threshold: 0.3
    });
  });
});