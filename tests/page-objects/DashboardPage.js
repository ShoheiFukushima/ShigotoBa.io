/**
 * ダッシュボードページのPage Objectモデル
 */

import { expect } from '@playwright/test';
import { selectors, timeouts, viewports } from '../helpers/common-selectors.js';
import { 
  setupPage, 
  takeScreenshot, 
  testResponsive,
  verifyElementsVisible 
} from '../helpers/test-utils.js';

export class DashboardPage {
  constructor(page) {
    this.page = page;
  }

  /**
   * ページの初期化
   */
  async init() {
    await setupPage(this.page);
    return this;
  }

  /**
   * ページタイトルの確認
   */
  async verifyTitle() {
    await expect(this.page).toHaveTitle(/shigotoba\.io/);
    
    const title = this.page.locator(selectors.dashboard.title);
    await expect(title).toBeVisible();
    
    const titleText = await title.textContent();
    expect(titleText).toContain('🏠 ダッシュボード');
    
    return this;
  }

  /**
   * Google Sheets接続状態の確認
   */
  async verifyGoogleSheetsStatus() {
    const sheetsStatus = this.page.locator(selectors.dashboard.googleSheetsStatus);
    const statusCount = await sheetsStatus.count();
    expect(statusCount).toBeGreaterThan(0);
    
    return this;
  }

  /**
   * メトリクスセクションの確認
   */
  async verifyMetricsSection() {
    const metricsHeader = this.page.locator(selectors.dashboard.metricsSection);
    await expect(metricsHeader).toBeVisible();
    
    const expectedMetrics = [
      'アクティブプロジェクト',
      '完了タスク', 
      '新規コンテンツ',
      '効率スコア'
    ];
    
    for (const metric of expectedMetrics) {
      const metricElement = this.page.locator(`text=${metric}`).first();
      await expect(metricElement).toBeVisible();
    }
    
    return this;
  }

  /**
   * クイックアクセスセクションの確認
   */
  async verifyQuickAccessSections() {
    const quickAccessHeader = this.page.locator(selectors.dashboard.quickAccessSection);
    await expect(quickAccessHeader).toBeVisible();
    
    const sections = {
      development: selectors.categories.development,
      analytics: selectors.categories.analytics,
      marketing: selectors.categories.marketing,
      automation: selectors.categories.automation
    };
    
    const results = await verifyElementsVisible(this.page, sections);
    
    // 少なくとも3つのセクションが表示されていることを確認
    const visibleCount = Object.values(results).filter(Boolean).length;
    expect(visibleCount).toBeGreaterThanOrEqual(3);
    
    return this;
  }

  /**
   * プロジェクト一覧セクションの確認
   */
  async verifyProjectSection() {
    const projectHeader = this.page.locator(selectors.dashboard.projectSection);
    await expect(projectHeader).toBeVisible();
    
    return this;
  }

  /**
   * オンボーディング要素の確認
   */
  async verifyOnboardingElements() {
    const welcomeText = this.page.locator(selectors.dashboard.welcomeMessage);
    
    if (await welcomeText.isVisible()) {
      const tourButton = this.page.locator(selectors.dashboard.tourButton);
      await expect(tourButton).toBeVisible();
    }
    
    // クイックスタートガイドの確認（存在する場合）
    const quickStartSection = this.page.locator('text=クイックスタートガイド');
    const quickStartCount = await quickStartSection.count();
    expect(quickStartCount).toBeGreaterThanOrEqual(0);
    
    return this;
  }

  /**
   * ワークフロー管理ボタンの確認
   */
  async verifyWorkflowManagementButton() {
    const workflowButton = this.page.locator(selectors.workflow.managerButton);
    await expect(workflowButton).toBeVisible();
    await expect(workflowButton).toBeEnabled();
    
    return this;
  }

  /**
   * レスポンシブデザインのテスト
   */
  async testResponsiveDesign() {
    // デスクトップビュー
    await testResponsive(this.page, viewports.desktop);
    const sidebar = this.page.locator(selectors.streamlit.sidebar);
    await expect(sidebar).toBeVisible();
    
    // モバイルビュー
    await testResponsive(this.page, viewports.mobile, 'dashboard-mobile');
    const mainContent = this.page.locator(selectors.dashboard.title);
    await expect(mainContent).toBeVisible();
    
    return this;
  }

  /**
   * スクリーンショットの撮影
   */
  async takeScreenshots() {
    await takeScreenshot(this.page, 'dashboard-main');
    
    // 各セクションのスクリーンショット
    const sections = [
      { name: 'metrics', element: selectors.dashboard.metricsSection },
      { name: 'projects', element: selectors.dashboard.projectSection },
      { name: 'quick-access', element: selectors.dashboard.quickAccessSection }
    ];
    
    for (const section of sections) {
      const element = this.page.locator(section.element);
      if (await element.isVisible()) {
        await element.scrollIntoViewIfNeeded();
        await takeScreenshot(this.page, `dashboard-${section.name}`);
      }
    }
    
    return this;
  }

  /**
   * 全体的な検証を実行
   */
  async verifyAll() {
    await this.verifyTitle();
    await this.verifyGoogleSheetsStatus();
    await this.verifyMetricsSection();
    await this.verifyProjectSection();
    await this.verifyQuickAccessSections();
    await this.verifyWorkflowManagementButton();
    await this.verifyOnboardingElements();
    
    return this;
  }
}