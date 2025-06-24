const { test, expect } = require('@playwright/test');

test.describe('Marketing Flow Navigation', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // テスト用プロジェクトを作成
    await page.click('text=📂 プロジェクト管理');
    await page.waitForTimeout(1000);
    
    const projectNameInput = page.locator('input[placeholder*="AI News Tool"]');
    await projectNameInput.fill('フローテストプロジェクト');
    await page.click('text=➕ 新規作成');
    
    await expect(page.locator('text=✅ プロジェクト \'フローテストプロジェクト\' を作成しました')).toBeVisible({ timeout: 10000 });
  });

  test('should navigate through product input stage', async ({ page }) => {
    // ステージ0: プロダクト入力が表示されているか確認
    const stageHeader = page.locator('text=📝 プロダクト情報入力');
    await expect(stageHeader).toBeVisible();
    
    // 入力フィールドが表示されているか確認
    const productNameInput = page.locator('input[placeholder*="AI News Curator"]');
    await expect(productNameInput).toBeVisible();
    
    const categorySelect = page.locator('select').first();
    await expect(categorySelect).toBeVisible();
    
    const targetInput = page.locator('input[placeholder*="ビジネスパーソン"]');
    await expect(targetInput).toBeVisible();
    
    const priceInput = page.locator('input[placeholder*="月額980円"]');
    await expect(priceInput).toBeVisible();
    
    const uniqueValueTextarea = page.locator('textarea[placeholder*="競合にない強み"]');
    await expect(uniqueValueTextarea).toBeVisible();
    
    // フォームに入力
    await productNameInput.fill('テストAIツール');
    await categorySelect.selectOption('ビジネスツール');
    await targetInput.fill('中小企業経営者');
    await priceInput.fill('月額1980円');
    await uniqueValueTextarea.fill('AIによる自動分析機能');
    
    // 次へボタンをクリック
    const nextButton = page.locator('text=次へ: 調査開始 →');
    await expect(nextButton).toBeVisible();
    await nextButton.click();
    
    // ステージ1に移動したか確認
    const stage1Header = page.locator('text=🔍 調査フェーズ開始');
    await expect(stage1Header).toBeVisible({ timeout: 10000 });
  });

  test('should show validation error for required fields', async ({ page }) => {
    // 必須フィールドを空のまま次へボタンをクリック
    const nextButton = page.locator('text=次へ: 調査開始 →');
    await nextButton.click();
    
    // エラーメッセージが表示されるか確認
    const errorMessage = page.locator('text=プロダクト名とカテゴリは必須です');
    await expect(errorMessage).toBeVisible();
  });

  test('should progress through multiple stages', async ({ page }) => {
    // Stage 0: プロダクト入力
    await page.locator('input[placeholder*="AI News Curator"]').fill('マルチステージテスト');
    await page.locator('select').first().selectOption('情報収集・配信');
    await page.locator('text=次へ: 調査開始 →').click();
    
    // Stage 1: 調査フェーズ
    await expect(page.locator('text=🔍 調査フェーズ開始')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=✅ 調査完了！')).toBeVisible();
    await page.locator('text=次へ: ベンチマーク策定 →').click();
    
    // Stage 2: ベンチマーク策定
    await expect(page.locator('text=📊 品質ベンチマーク策定')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=✅ ベンチマーク作成完了！')).toBeVisible();
    await page.locator('text=次へ: ベネフィット決定 →').click();
    
    // Stage 3: ベネフィット決定
    await expect(page.locator('text=💡 ベネフィット決定')).toBeVisible({ timeout: 10000 });
    await page.locator('text=次へ: マーケティング施策 →').click();
    
    // Stage 4: マーケティング施策
    await expect(page.locator('text=🎯 マーケティング施策立案')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=✅ 戦略的キャンペーン生成完了！')).toBeVisible();
    
    // プログレスバーが更新されているか確認
    const progressBar = page.locator('.progress-bar');
    await expect(progressBar).toBeVisible();
    
    // 進捗が50%以上になっているか確認（Stage 4は50%）
    const progressText = page.locator('.progress-bar:has-text("57%")');
    await expect(progressText).toBeVisible();
  });

  test('should show stage navigation buttons', async ({ page }) => {
    // 全ステージボタンが表示されているか確認
    const stage0Button = page.locator('button:has-text("📝\nプロダクト入力")');
    await expect(stage0Button).toBeVisible();
    await expect(stage0Button).not.toBeDisabled();
    
    const stage1Button = page.locator('button:has-text("🔍\n調査フェーズ")');
    await expect(stage1Button).toBeVisible();
    // ステージ1は最初は無効化されている
    await expect(stage1Button).toBeDisabled();
    
    // プロダクト入力を完了
    await page.locator('input[placeholder*="AI News Curator"]').fill('ナビゲーションテスト');
    await page.locator('select').first().selectOption('タスク管理');
    await page.locator('text=次へ: 調査開始 →').click();
    
    // ステージ1に進んだ後、ステージ0ボタンをクリックして戻れるか確認
    await expect(page.locator('text=🔍 調査フェーズ開始')).toBeVisible({ timeout: 10000 });
    await stage0Button.click();
    
    // ステージ0に戻ったか確認
    await expect(page.locator('text=📝 プロダクト情報入力')).toBeVisible({ timeout: 10000 });
  });

  test('should preserve data when switching stages', async ({ page }) => {
    // プロダクト情報を入力
    const productName = 'データ保持テスト';
    await page.locator('input[placeholder*="AI News Curator"]').fill(productName);
    await page.locator('select').first().selectOption('教育');
    await page.locator('input[placeholder*="ビジネスパーソン"]').fill('学生');
    await page.locator('text=次へ: 調査開始 →').click();
    
    // ステージ1に移動
    await expect(page.locator('text=🔍 調査フェーズ開始')).toBeVisible({ timeout: 10000 });
    
    // プロダクト情報が表示されているか確認
    const productInfo = page.locator(`text=**プロダクト**: ${productName}`);
    await expect(productInfo).toBeVisible();
    
    const categoryInfo = page.locator('text=**カテゴリ**: 教育');
    await expect(categoryInfo).toBeVisible();
    
    // ステージ0に戻る
    const stage0Button = page.locator('button:has-text("📝\nプロダクト入力")');
    await stage0Button.click();
    
    // 入力データが保持されているか確認
    const savedProductName = page.locator(`input[value="${productName}"]`);
    await expect(savedProductName).toBeVisible();
  });
});