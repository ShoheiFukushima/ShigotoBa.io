import { test, expect } from '@playwright/test';
import { WorkflowPage } from '../page-objects/WorkflowPage.js';

test.describe('ワークフロー管理機能 - リファクタリング版', () => {
  let workflowPage;

  test.beforeEach(async ({ page }) => {
    workflowPage = new WorkflowPage(page);
    await workflowPage.init();
  });

  test('ワークフロー管理ページへの遷移とスクリーンショット', async () => {
    await workflowPage.navigateToWorkflowManager();
  });

  test('ワークフロー詳細表示機能のテスト', async () => {
    await workflowPage.testWorkflowDetails();
  });

  test('統合サマリーボタンの確認', async () => {
    await workflowPage.verifySummaryButton();
  });

  test('AIパイプラインボタンの確認', async () => {
    await workflowPage.verifyPipelineButton();
  });

  test('モバイルビューでのレスポンシブ確認', async () => {
    await workflowPage.testMobileResponsive();
  });

  test('ページ全体のビジュアルリグレッション', async () => {
    await workflowPage.captureVisualRegression();
  });

  test('ワークフロー機能全体の統合テスト', async () => {
    await workflowPage.verifyAll();
  });

  test.afterEach(async ({ page }, testInfo) => {
    await workflowPage.captureFailureScreenshot(testInfo);
  });
});