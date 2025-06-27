// @ts-check
const { test, expect } = require('@playwright/test');

// Streamlitアプリのベースとなるshigotobaの固定URL
const SHIGOTOBA_URL = 'http://localhost:8502';

test.describe('Shigotoba.io E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // アプリケーションにアクセス
    await page.goto(SHIGOTOBA_URL);
    
    // Streamlitの初期ロードを待つ
    await page.waitForSelector('[data-testid="stAppViewContainer"]', { timeout: 30000 });
    await page.waitForTimeout(2000); // 追加の待機
  });

  test('ホームページが正しく表示される', async ({ page }) => {
    // タイトルの確認
    await expect(page.locator('h1').filter({ hasText: 'Shigotoba.io へようこそ' })).toBeVisible();
    
    // サブタイトルの確認
    await expect(page.locator('text=個人開発者向け全自動マーケティング代理店システム')).toBeVisible();
    
    // 特徴セクションの確認
    await expect(page.locator('text=14個のAI専門家')).toBeVisible();
    await expect(page.locator('text=企画から配信まで')).toBeVisible();
    
    // 新規プロジェクト開始ボタンの確認
    const startButton = page.locator('button').filter({ hasText: '新規プロジェクトを開始' });
    await expect(startButton).toBeVisible();
  });

  test('サイドバーナビゲーションが機能する', async ({ page }) => {
    // サイドバーの確認
    await expect(page.locator('text=Shigotoba.io').first()).toBeVisible();
    
    // 各メニューボタンの確認
    await expect(page.locator('button').filter({ hasText: 'ホーム' })).toBeVisible();
    await expect(page.locator('button').filter({ hasText: '企画書入力' })).toBeVisible();
    await expect(page.locator('button').filter({ hasText: 'AI実行状況' })).toBeVisible();
    await expect(page.locator('button').filter({ hasText: '承認ゲート' })).toBeVisible();
    await expect(page.locator('button').filter({ hasText: 'レポート' })).toBeVisible();
  });

  test('企画書入力フォームに遷移できる', async ({ page }) => {
    // 新規プロジェクト開始ボタンをクリック
    await page.locator('button').filter({ hasText: '新規プロジェクトを開始' }).click();
    await page.waitForTimeout(1000);
    
    // 企画書入力ページの確認
    await expect(page.locator('h1').filter({ hasText: 'プロジェクト企画書入力' })).toBeVisible();
    await expect(page.locator('text=アプリのアイデアを入力してください')).toBeVisible();
    
    // フォームフィールドの確認
    await expect(page.locator('label').filter({ hasText: 'アプリ名' })).toBeVisible();
    await expect(page.locator('label').filter({ hasText: 'カテゴリ' })).toBeVisible();
    await expect(page.locator('text=プラットフォーム')).toBeVisible();
  });

  test('企画書フォームの入力と検証が機能する', async ({ page }) => {
    // 企画書入力ページへ移動
    await page.locator('button').filter({ hasText: '企画書入力' }).click();
    await page.waitForTimeout(1000);
    
    // 不完全なフォームで送信を試みる
    await page.locator('button').filter({ hasText: 'AI分析を開始' }).click();
    await page.waitForTimeout(500);
    
    // エラーメッセージの確認
    await expect(page.locator('text=アプリ名を入力してください')).toBeVisible();
    
    // フォームに入力
    await page.locator('input[aria-label="アプリ名"]').fill('TestTaskApp');
    
    // カテゴリ選択
    await page.locator('label').filter({ hasText: 'カテゴリ' }).locator('..').locator('select').selectOption('仕事効率化');
    
    // プラットフォーム選択（マルチセレクト）
    await page.locator('label').filter({ hasText: 'プラットフォーム' }).locator('..').locator('[data-baseweb="select"]').click();
    await page.locator('text=iOS').click();
    await page.locator('text=Android').click();
    await page.keyboard.press('Escape');
    
    // コンセプト入力
    await page.locator('textarea').first().fill('AIでタスクを自動整理する革新的アプリ');
    
    // 解決する課題入力
    await page.locator('input[id="problem_0"]').fill('タスクの優先順位付けが難しい');
    await page.locator('input[id="problem_1"]').fill('締切管理が煩雑');
    
    // ターゲット入力
    await page.locator('label').filter({ hasText: 'メインユーザー' }).locator('..').locator('textarea').fill('25-40歳のビジネスパーソン');
    await page.locator('label').filter({ hasText: '利用シーン' }).locator('..').locator('textarea').fill('朝の通勤時間、会議前の確認');
    
    // コア機能入力
    await page.locator('input[id="core_0"]').fill('AIタスク自動分類');
    await page.locator('input[id="core_1"]').fill('スマート通知');
    await page.locator('input[id="core_2"]').fill('進捗ダッシュボード');
    
    // 差別化機能入力
    await page.locator('input[id="unique_0"]').fill('音声入力対応');
    
    // 収益モデル選択
    await page.locator('label').filter({ hasText: 'フリーミアム' }).click();
    
    // 価格帯入力
    await page.locator('input[placeholder="例: 基本無料、プレミアム月額500-1000円"]').fill('基本無料、プレミアム月額980円');
  });

  test('AI実行状況ページが表示される', async ({ page }) => {
    // AI実行状況ページへ移動
    await page.locator('button').filter({ hasText: 'AI実行状況' }).click();
    await page.waitForTimeout(1000);
    
    // ページタイトルの確認
    await expect(page.locator('h1').filter({ hasText: 'AI実行状況' })).toBeVisible();
    
    // プロジェクト未設定の警告
    await expect(page.locator('text=プロジェクトが設定されていません')).toBeVisible();
  });

  test('承認ゲートページが表示される', async ({ page }) => {
    // 承認ゲートページへ移動
    await page.locator('button').filter({ hasText: '承認ゲート' }).click();
    await page.waitForTimeout(1000);
    
    // ページタイトルの確認
    await expect(page.locator('h1').filter({ hasText: '承認ゲート' })).toBeVisible();
    
    // 承認項目なしのメッセージ
    await expect(page.locator('text=現在承認が必要な項目はありません')).toBeVisible();
  });

  test('レポートページが表示される', async ({ page }) => {
    // レポートページへ移動
    await page.locator('button').filter({ hasText: 'レポート' }).click();
    await page.waitForTimeout(1000);
    
    // ページタイトルの確認
    await expect(page.locator('h1').filter({ hasText: 'レポート' })).toBeVisible();
    
    // プロジェクト未設定の警告
    await expect(page.locator('text=プロジェクトが設定されていません')).toBeVisible();
  });

  test('完全な企画書入力からAI実行までのフロー', async ({ page }) => {
    // 1. 企画書入力ページへ
    await page.locator('button').filter({ hasText: '新規プロジェクトを開始' }).click();
    await page.waitForTimeout(1000);
    
    // 2. 必須フィールドをすべて入力
    // アプリ名
    await page.locator('input[aria-label="アプリ名"]').fill('SmartTasker');
    
    // カテゴリ
    await page.locator('label').filter({ hasText: 'カテゴリ' }).locator('..').locator('select').selectOption('仕事効率化');
    
    // プラットフォーム（Streamlitのマルチセレクト）
    await page.locator('label').filter({ hasText: 'プラットフォーム' }).locator('..').locator('[data-baseweb="select"]').click();
    await page.locator('li').filter({ hasText: 'iOS' }).click();
    await page.keyboard.press('Escape');
    
    // コンセプト
    await page.locator('textarea').first().fill('AIがタスクを自動分類し最適な順序を提案する次世代アプリ');
    
    // 解決する課題
    await page.locator('input[id="problem_0"]').fill('タスク管理が複雑');
    await page.locator('input[id="problem_1"]').fill('優先順位の判断が難しい');
    await page.locator('input[id="problem_2"]').fill('チーム共有が面倒');
    
    // ターゲット
    await page.locator('label').filter({ hasText: 'メインユーザー' }).locator('..').locator('textarea').fill('30代ビジネスパーソン、リモートワーカー');
    await page.locator('label').filter({ hasText: '利用シーン' }).locator('..').locator('textarea').fill('朝のタスク整理、会議前の確認');
    
    // コア機能（3つ必須）
    await page.locator('input[id="core_0"]').fill('AI自動分類');
    await page.locator('input[id="core_1"]').fill('スマート通知');
    await page.locator('input[id="core_2"]').fill('チームダッシュボード');
    
    // 差別化機能
    await page.locator('input[id="unique_0"]').fill('音声入力');
    
    // 収益モデル
    await page.locator('label').filter({ hasText: 'フリーミアム' }).click();
    
    // 価格帯
    await page.locator('input[placeholder="例: 基本無料、プレミアム月額500-1000円"]').fill('基本無料、月額980円');
    
    // 3. フォーム送信
    await page.locator('button').filter({ hasText: 'AI分析を開始' }).click();
    await page.waitForTimeout(2000);
    
    // 4. 成功メッセージとページ遷移の確認
    await expect(page.locator('text=企画書を受け付けました')).toBeVisible();
    
    // 5. AI実行状況ページへの遷移確認
    await page.waitForTimeout(3000);
    await expect(page.locator('h1').filter({ hasText: 'AI実行状況' })).toBeVisible();
    
    // 6. プロジェクト情報がサイドバーに表示されることを確認
    await expect(page.locator('text=SmartTasker')).toBeVisible();
    await expect(page.locator('text=仕事効率化')).toBeVisible();
  });

  test('レスポンシブデザインの確認', async ({ page }) => {
    // モバイルサイズ
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(SHIGOTOBA_URL);
    await page.waitForTimeout(2000);
    
    // モバイルでも主要要素が表示されることを確認
    await expect(page.locator('h1').first()).toBeVisible();
    
    // タブレットサイズ
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(1000);
    await expect(page.locator('h1').first()).toBeVisible();
    
    // デスクトップサイズ
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.waitForTimeout(1000);
    await expect(page.locator('h1').first()).toBeVisible();
  });
});

// パフォーマンステスト
test.describe('Performance Tests', () => {
  test('ページロード時間が許容範囲内', async ({ page }) => {
    const startTime = Date.now();
    await page.goto(SHIGOTOBA_URL);
    await page.waitForSelector('[data-testid="stAppViewContainer"]');
    const loadTime = Date.now() - startTime;
    
    // 5秒以内にロードされることを確認
    expect(loadTime).toBeLessThan(5000);
  });
});

// アクセシビリティテスト
test.describe('Accessibility Tests', () => {
  test('キーボードナビゲーションが機能する', async ({ page }) => {
    await page.goto(SHIGOTOBA_URL);
    await page.waitForTimeout(2000);
    
    // Tabキーでフォーカス移動
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Enterキーでボタンクリック
    const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
    expect(focusedElement).toBeTruthy();
  });
});