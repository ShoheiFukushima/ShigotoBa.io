import { test, expect } from '@playwright/test';
import { DashboardPage } from '../page-objects/DashboardPage.js';

test.describe('shigotoba.io ダッシュボード - リファクタリング版', () => {
  let dashboardPage;

  test.beforeEach(async ({ page }) => {
    dashboardPage = new DashboardPage(page);
    await dashboardPage.init();
  });

  test('ダッシュボードの基本表示テスト', async () => {
    await dashboardPage.verifyTitle();
  });

  test('Google Sheets接続状態の表示', async () => {
    await dashboardPage.verifyGoogleSheetsStatus();
  });

  test('メトリクスセクションの表示', async () => {
    await dashboardPage.verifyMetricsSection();
  });

  test('プロジェクト一覧セクションの表示', async () => {
    await dashboardPage.verifyProjectSection();
  });

  test('クイックアクセスセクションの表示', async () => {
    await dashboardPage.verifyQuickAccessSections();
  });

  test('ワークフロー管理ボタンの表示', async () => {
    await dashboardPage.verifyWorkflowManagementButton();
  });

  test('オンボーディング要素の表示', async () => {
    await dashboardPage.verifyOnboardingElements();
  });

  test('レスポンシブデザインのテスト', async () => {
    await dashboardPage.testResponsiveDesign();
  });

  test('ダッシュボード全体の統合テスト', async () => {
    await dashboardPage.verifyAll();
    await dashboardPage.takeScreenshots();
  });
});