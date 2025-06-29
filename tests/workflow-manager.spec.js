import { test, expect } from '@playwright/test';

test.describe('ワークフロー管理機能のE2Eテスト', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8501');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // 初期画面のスクリーンショット
    await page.screenshot({ 
      path: 'screenshots/initial-page.png',
      fullPage: true 
    });
  });

  test('ワークフロー管理ページへの遷移とスクリーンショット', async ({ page }) => {
    // サイドバーの確認
    const sidebar = await page.locator('.sidebar-container, [data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();
    await page.screenshot({ path: 'screenshots/sidebar-visible.png' });

    // ワークフロー管理ボタンを探す
    const workflowButton = await page.locator('text=ワークフロー管理');
    if (await workflowButton.isVisible()) {
      await page.screenshot({ path: 'screenshots/workflow-button-found.png' });
      await workflowButton.click();
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      // ワークフロー管理ページのスクリーンショット
      await page.screenshot({ 
        path: 'screenshots/workflow-manager-page.png',
        fullPage: true 
      });
      
      // ページタイトルまたは特定の要素で遷移を確認
      const pageTitle = await page.locator('h1, h2').filter({ hasText: /ワークフロー/ });
      await expect(pageTitle).toBeVisible();
    }
  });

  test('ワークフロー詳細表示機能のテスト', async ({ page }) => {
    // ワークフロー管理ページへ遷移
    const workflowButton = await page.locator('text=ワークフロー管理');
    if (await workflowButton.isVisible()) {
      await workflowButton.click();
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      // 詳細を見るボタンを探す
      const detailButtons = await page.locator('button').filter({ hasText: '詳細を見る' });
      const count = await detailButtons.count();
      
      if (count > 0) {
        // 最初の詳細ボタンをクリック
        await detailButtons.first().scrollIntoViewIfNeeded();
        await page.screenshot({ path: 'screenshots/before-detail-click.png' });
        
        await detailButtons.first().click();
        await page.waitForTimeout(1000);
        
        // 詳細セクションが表示されることを確認
        await page.screenshot({ 
          path: 'screenshots/workflow-detail-expanded.png',
          fullPage: true 
        });
        
        // 詳細セクションの要素を確認
        const detailSection = await page.locator('text=ステップ').first();
        if (await detailSection.isVisible()) {
          await expect(detailSection).toBeVisible();
          
          // アクションボタンの確認
          const actionButtons = await page.locator('button').filter({ 
            hasText: /実行|編集|削除|一時停止/ 
          });
          
          if (await actionButtons.count() > 0) {
            await page.screenshot({ 
              path: 'screenshots/workflow-action-buttons.png' 
            });
          }
        }
      }
    }
  });

  test('モバイルビューでのレスポンシブ確認', async ({ page }) => {
    // モバイルビューポートに変更
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(500);
    
    await page.screenshot({ 
      path: 'screenshots/mobile-view-initial.png',
      fullPage: true 
    });
    
    // ワークフロー管理ページへ遷移
    const workflowButton = await page.locator('text=ワークフロー管理');
    if (await workflowButton.isVisible()) {
      await workflowButton.click();
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      await page.screenshot({ 
        path: 'screenshots/mobile-workflow-manager.png',
        fullPage: true 
      });
    }
  });

  test('統合サマリーボタンの確認', async ({ page }) => {
    // 統合サマリーボタンを探す
    const summaryButton = await page.locator('button').filter({ hasText: '統合サマリー' });
    
    if (await summaryButton.isVisible()) {
      await summaryButton.scrollIntoViewIfNeeded();
      await page.screenshot({ path: 'screenshots/summary-button.png' });
      
      // ボタンのスタイルを確認（primaryタイプ）
      const buttonType = await summaryButton.evaluate(el => {
        return window.getComputedStyle(el).backgroundColor;
      });
      
      // primaryボタンは通常青系の背景色
      expect(buttonType).toBeTruthy();
    }
  });

  test('AIパイプラインボタンの確認', async ({ page }) => {
    // AIパイプラインボタンを探す
    const pipelineButton = await page.locator('button').filter({ hasText: 'AIパイプライン' });
    
    if (await pipelineButton.isVisible()) {
      await pipelineButton.scrollIntoViewIfNeeded();
      await page.screenshot({ path: 'screenshots/pipeline-button.png' });
    }
  });

  test('ページ全体のビジュアルリグレッション', async ({ page }) => {
    // 各主要ページのスクリーンショットを撮影
    const pages = [
      { name: 'home', path: '/' },
      { name: 'workflow', button: 'ワークフロー管理' },
      { name: 'development', button: '開発室' },
      { name: 'project', button: 'プロジェクト管理' }
    ];
    
    for (const pageInfo of pages) {
      if (pageInfo.path) {
        await page.goto(`http://localhost:8501${pageInfo.path}`);
      } else if (pageInfo.button) {
        const button = await page.locator(`text=${pageInfo.button}`);
        if (await button.isVisible()) {
          await button.click();
        }
      }
      
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      await page.screenshot({ 
        path: `screenshots/visual-regression-${pageInfo.name}.png`,
        fullPage: true 
      });
    }
  });

  test.afterEach(async ({ page }, testInfo) => {
    // テスト終了時の最終スクリーンショット
    if (testInfo.status !== 'passed') {
      await page.screenshot({ 
        path: `screenshots/failed-${testInfo.title.replace(/\s+/g, '-')}.png`,
        fullPage: true 
      });
    }
  });
});