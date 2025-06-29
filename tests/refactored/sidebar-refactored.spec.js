import { test, expect } from '@playwright/test';
import { SidebarPage } from '../page-objects/SidebarPage.js';

test.describe('Streamlitサイドバー - リファクタリング版', () => {
  let sidebarPage;

  test.beforeEach(async ({ page }) => {
    sidebarPage = new SidebarPage(page);
    await sidebarPage.init();
  });

  test('サイドバーの基本表示', async () => {
    await sidebarPage.verifyBranding();
  });

  test('メニューナビゲーション機能', async () => {
    await sidebarPage.verifyMenuNavigation();
  });

  test('プロジェクトセレクターの動作', async () => {
    await sidebarPage.verifyProjectSelector();
  });

  test('統計情報の表示', async () => {
    await sidebarPage.verifyStatistics();
  });

  test('クイックアクションボタン', async () => {
    await sidebarPage.verifyQuickActions();
  });

  test('フッターの表示', async () => {
    await sidebarPage.verifyFooter();
  });

  test('レスポンシブ動作の確認', async () => {
    await sidebarPage.testResponsive();
  });

  test('ページ遷移の動作', async () => {
    await sidebarPage.testPageNavigation();
  });

  test('メインナビゲーションとの統合', async () => {
    await sidebarPage.verifyIntegrationWithMain();
  });

  test('統計メトリクスの詳細確認', async () => {
    await sidebarPage.verifyDetailedStatistics();
  });

  test('サイドバー全体の統合テスト', async () => {
    await sidebarPage.verifyAll();
  });
});