// E2Eテスト - ダッシュボード全機能テスト
const { test, expect } = require('@playwright/test');

test.describe('マーケティング自動化ダッシュボード E2E テスト', () => {
  
  test.beforeEach(async ({ page }) => {
    // ダッシュボードにアクセス
    await page.goto('/');
    // ページロードを待機
    await page.waitForLoadState('networkidle');
  });

  test('ホーム画面の基本表示確認', async ({ page }) => {
    // ページタイトル確認
    await expect(page).toHaveTitle(/ダッシュボード/);
    
    // 挨拶メッセージ確認（名前なし）
    const greeting = page.locator('.greeting');
    await expect(greeting).toBeVisible();
    await expect(greeting).not.toContainText('福島');
    
    // メトリクス表示確認
    await expect(page.locator('text=アクティブプロジェクト')).toBeVisible();
    await expect(page.locator('text=未完了タスク')).toBeVisible();
    await expect(page.locator('text=今週の成果')).toBeVisible();
    await expect(page.locator('text=効率スコア')).toBeVisible();
  });

  test('クイックアクセス - 3つのカテゴリ表示確認', async ({ page }) => {
    // プロジェクト開発カテゴリ
    await expect(page.locator('text=🏗️ プロジェクト開発')).toBeVisible();
    await expect(page.locator('text=開発室')).toBeVisible();
    await expect(page.locator('text=プロジェクト\\n管理室')).toBeVisible();
    
    // プロジェクト運営・分析カテゴリ
    await expect(page.locator('text=📈 プロジェクト運営・分析')).toBeVisible();
    await expect(page.locator('text=パフォーマンス')).toBeVisible();
    await expect(page.locator('text=アトリビューション\\n分析')).toBeVisible();
    
    // 広告・マーケティング実行カテゴリ
    await expect(page.locator('text=🎨 広告・マーケティング実行')).toBeVisible();
    await expect(page.locator('text=AI Creative\\nStudio')).toBeVisible();
    await expect(page.locator('text=リアルタイム\\n最適化')).toBeVisible();
  });

  test('ドキュメント書庫 - ツリー表示確認', async ({ page }) => {
    // ドキュメント書庫セクション確認
    await expect(page.locator('text=📚 ドキュメント書庫')).toBeVisible();
    
    // 3つのカテゴリ確認
    await expect(page.locator('text=📋 マニュアル・ガイド')).toBeVisible();
    await expect(page.locator('text=📊 レポート・分析')).toBeVisible();
    await expect(page.locator('text=🎨 クリエイティブ素材')).toBeVisible();
    
    // ツリー構造のアイテム確認
    await expect(page.locator('text=システム利用ガイド')).toBeVisible();
    await expect(page.locator('text=2024年Q4実績レポート')).toBeVisible();
    await expect(page.locator('text=ブランドガイドライン')).toBeVisible();
  });

  test('プロジェクト管理室への遷移', async ({ page }) => {
    // プロジェクト管理室ボタンクリック
    await page.locator('text=プロジェクト\\n管理室').click();
    
    // ページ遷移確認
    await page.waitForLoadState('networkidle');
    await expect(page.locator('text=プロジェクト管理室')).toBeVisible();
    
    // パンくずリストでホームに戻る
    const homeLink = page.locator('text=🏠 ホーム');
    if (await homeLink.isVisible()) {
      await homeLink.click();
      await page.waitForLoadState('networkidle');
      await expect(page.locator('.greeting')).toBeVisible();
    }
  });

  test('AI Creative Studioへの遷移', async ({ page }) => {
    // AI Creative Studioボタンクリック
    await page.locator('text=AI Creative\\nStudio').click();
    
    // ページ遷移確認
    await page.waitForLoadState('networkidle');
    await expect(page.locator('text=AI Creative Studio')).toBeVisible();
    
    // 主要機能の表示確認
    await expect(page.locator('text=クリエイティブタイプ')).toBeVisible();
    await expect(page.locator('text=ターゲットオーディエンス')).toBeVisible();
  });

  test('リアルタイム最適化への遷移', async ({ page }) => {
    // リアルタイム最適化ボタンクリック
    await page.locator('text=リアルタイム\\n最適化').click();
    
    // ページ遷移確認
    await page.waitForLoadState('networkidle');
    await expect(page.locator('text=リアルタイム広告最適化')).toBeVisible();
    
    // 最適化機能の表示確認
    await expect(page.locator('text=最適化エンジン')).toBeVisible();
  });

  test('A/Bテストページの動作確認', async ({ page }) => {
    // A/Bテストボタンクリック
    await page.locator('text=A/Bテスト').click();
    
    // ページ遷移確認
    await page.waitForLoadState('networkidle');
    await expect(page.locator('text=A/Bテスト自動化')).toBeVisible();
    
    // 統計機能の表示確認
    await expect(page.locator('text=統計的有意性')).toBeVisible();
    await expect(page.locator('text=サンプルサイズ計算')).toBeVisible();
  });

  test('パフォーマンスダッシュボードの表示', async ({ page }) => {
    // パフォーマンスボタンクリック
    await page.locator('text=パフォーマンス').click();
    
    // ページ遷移確認
    await page.waitForLoadState('networkidle');
    await expect(page.locator('text=パフォーマンス追跡ダッシュボード')).toBeVisible();
    
    // KPI表示確認
    await expect(page.locator('text=コンバージョン率')).toBeVisible();
    await expect(page.locator('text=ROI')).toBeVisible();
  });

  test('サイドバー機能の確認', async ({ page }) => {
    // サイドバーの表示確認
    await expect(page.locator('text=⚡ クイックアクション')).toBeVisible();
    await expect(page.locator('text=➕ 新規プロジェクト')).toBeVisible();
    
    // 統計セクションの確認
    await expect(page.locator('text=📊 今週の統計')).toBeVisible();
    await expect(page.locator('text=完了タスク')).toBeVisible();
    
    // 通知セクションの確認
    await expect(page.locator('text=🔔 通知')).toBeVisible();
  });

  test('レスポンシブデザインの確認', async ({ page }) => {
    // デスクトップサイズでの表示確認
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page.locator('.greeting')).toBeVisible();
    
    // タブレットサイズでの表示確認
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page.locator('.greeting')).toBeVisible();
    
    // モバイルサイズでの表示確認
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('.greeting')).toBeVisible();
  });

  test('エラーページの存在確認', async ({ page }) => {
    // 存在しないページにアクセス
    const response = await page.goto('/nonexistent-page');
    
    // 404エラーまたはStreamlitのデフォルトエラー処理を確認
    expect(response?.status()).toBe(404);
  });

  test('ページ読み込み時間の確認', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    // 10秒以内にロードされることを確認
    expect(loadTime).toBeLessThan(10000);
  });

  test('多機能ページの統合テスト', async ({ page }) => {
    // ホーム → プロジェクト管理 → 開発室 → ホームの循環テスト
    
    // プロジェクト管理室へ
    await page.locator('text=プロジェクト\\n管理室').click();
    await page.waitForLoadState('networkidle');
    await expect(page.locator('text=プロジェクト管理室')).toBeVisible();
    
    // 開発室へ（サイドバーまたはリンクから）
    const devRoomButton = page.locator('text=開発室').first();
    if (await devRoomButton.isVisible()) {
      await devRoomButton.click();
      await page.waitForLoadState('networkidle');
      await expect(page.locator('text=開発室')).toBeVisible();
    }
    
    // ホームに戻る
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('.greeting')).toBeVisible();
  });

});

test.describe('広告代理店機能 E2E テスト', () => {
  
  test('AI Creative Studio - 全機能テスト', async ({ page }) => {
    await page.goto('/');
    await page.locator('text=AI Creative\\nStudio').click();
    await page.waitForLoadState('networkidle');
    
    // クリエイティブ生成のテスト
    await expect(page.locator('text=広告コピー')).toBeVisible();
    await expect(page.locator('text=SNSコンテンツ')).toBeVisible();
    await expect(page.locator('text=動画スクリプト')).toBeVisible();
    await expect(page.locator('text=メールキャンペーン')).toBeVisible();
  });

  test('マルチプラットフォーム - 統合管理テスト', async ({ page }) => {
    await page.goto('/');
    await page.locator('text=マルチ\\nプラットフォーム').click();
    await page.waitForLoadState('networkidle');
    
    // プラットフォーム管理の確認
    await expect(page.locator('text=Google Ads')).toBeVisible();
    await expect(page.locator('text=Facebook')).toBeVisible();
    await expect(page.locator('text=Instagram')).toBeVisible();
    await expect(page.locator('text=Twitter')).toBeVisible();
  });

  test('アトリビューション分析 - 高度な分析テスト', async ({ page }) => {
    await page.goto('/');
    await page.locator('text=アトリビューション\\n分析').click();
    await page.waitForLoadState('networkidle');
    
    // アトリビューションモデルの確認
    await expect(page.locator('text=First-Touch')).toBeVisible();
    await expect(page.locator('text=Last-Touch')).toBeVisible();
    await expect(page.locator('text=Linear')).toBeVisible();
    await expect(page.locator('text=Time-Decay')).toBeVisible();
  });

  test('カスタマージャーニー - 予測エンジンテスト', async ({ page }) => {
    await page.goto('/');
    await page.locator('text=カスタマー\\nジャーニー').click();
    await page.waitForLoadState('networkidle');
    
    // ジャーニー分析の確認
    await expect(page.locator('text=顧客セグメンテーション')).toBeVisible();
    await expect(page.locator('text=チャーン予測')).toBeVisible();
    await expect(page.locator('text=ジャーニー最適化')).toBeVisible();
  });

});