/**
 * ワークフローページのPage Objectモデル
 */

import { expect } from '@playwright/test';
import { selectors, timeouts, viewports } from '../helpers/common-selectors.js';
import { 
  setupPage, 
  takeScreenshot, 
  clickAndWait,
  testResponsive,
  checkElementIfVisible 
} from '../helpers/test-utils.js';

export class WorkflowPage {
  constructor(page) {
    this.page = page;
  }

  /**
   * ページの初期化とスクリーンショット
   */
  async init() {
    await setupPage(this.page);
    await takeScreenshot(this.page, 'initial-page');
    
    return this;
  }

  /**
   * ワークフロー管理ページへの遷移
   */
  async navigateToWorkflowManager() {
    const sidebar = this.page.locator(selectors.streamlit.sidebar);
    await expect(sidebar).toBeVisible();
    await takeScreenshot(this.page, 'sidebar-visible');

    const workflowButton = this.page.locator(selectors.workflow.managerButton);
    
    if (await workflowButton.isVisible()) {
      await takeScreenshot(this.page, 'workflow-button-found');
      await workflowButton.click();
      await this.page.waitForTimeout(timeouts.long);
      
      await this.page.waitForLoadState('networkidle');
      await takeScreenshot(this.page, 'workflow-manager-page');
      
      const pageTitle = this.page.locator('h1, h2').filter({ hasText: /ワークフロー/ });
      await expect(pageTitle).toBeVisible();
    }
    
    return this;
  }

  /**
   * ワークフロー詳細表示機能のテスト
   */
  async testWorkflowDetails() {
    await this.navigateToWorkflowManager();
    
    const detailButtons = this.page.locator(selectors.workflow.detailButton);
    const count = await detailButtons.count();
    
    if (count > 0) {
      await detailButtons.first().scrollIntoViewIfNeeded();
      await takeScreenshot(this.page, 'before-detail-click');
      
      await detailButtons.first().click();
      await this.page.waitForTimeout(timeouts.long);
      
      await takeScreenshot(this.page, 'workflow-detail-expanded');
      
      const detailSection = this.page.locator(selectors.workflow.stepSection).first();
      
      if (await detailSection.isVisible()) {
        await expect(detailSection).toBeVisible();
        
        const actionButtons = this.page.locator(selectors.workflow.actionButtons);
        
        if (await actionButtons.count() > 0) {
          await takeScreenshot(this.page, 'workflow-action-buttons');
        }
      }
    }
    
    return this;
  }

  /**
   * 統合サマリーボタンの確認
   */
  async verifySummaryButton() {
    const summaryButton = this.page.locator('button').filter({ hasText: '統合サマリー' });
    
    await checkElementIfVisible(summaryButton, async (button) => {
      await button.scrollIntoViewIfNeeded();
      await takeScreenshot(this.page, 'summary-button');
      
      const buttonType = await button.evaluate(el => {
        return window.getComputedStyle(el).backgroundColor;
      });
      
      expect(buttonType).toBeTruthy();
    });
    
    return this;
  }

  /**
   * AIパイプラインボタンの確認
   */
  async verifyPipelineButton() {
    const pipelineButton = this.page.locator('button').filter({ hasText: 'AIパイプライン' });
    
    await checkElementIfVisible(pipelineButton, async (button) => {
      await button.scrollIntoViewIfNeeded();
      await takeScreenshot(this.page, 'pipeline-button');
    });
    
    return this;
  }

  /**
   * モバイルビューでのレスポンシブ確認
   */
  async testMobileResponsive() {
    await testResponsive(this.page, viewports.mobile, 'mobile-view-initial');
    
    const workflowButton = this.page.locator(selectors.workflow.managerButton);
    
    if (await workflowButton.isVisible()) {
      await workflowButton.click();
      await this.page.waitForTimeout(timeouts.long);
      
      await this.page.waitForLoadState('networkidle');
      await takeScreenshot(this.page, 'mobile-workflow-manager');
    }
    
    return this;
  }

  /**
   * ページ全体のビジュアルリグレッション
   */
  async captureVisualRegression() {
    const pages = [
      { name: 'home', path: '/' },
      { name: 'workflow', button: selectors.workflow.managerButton },
      { name: 'development', button: 'button:has-text("開発室")' },
      { name: 'project', button: 'button:has-text("プロジェクト管理")' }
    ];
    
    for (const pageInfo of pages) {
      if (pageInfo.path) {
        await this.page.goto(`http://localhost:8501${pageInfo.path}`);
      } else if (pageInfo.button) {
        const button = this.page.locator(pageInfo.button);
        if (await button.isVisible()) {
          await button.click();
          await this.page.waitForTimeout(timeouts.long);
        }
      }
      
      await this.page.waitForLoadState('networkidle');
      await takeScreenshot(this.page, `visual-regression-${pageInfo.name}`);
    }
    
    return this;
  }

  /**
   * 失敗時のスクリーンショット撮影
   */
  async captureFailureScreenshot(testInfo) {
    if (testInfo.status !== 'passed') {
      await takeScreenshot(
        this.page, 
        `failed-${testInfo.title.replace(/\s+/g, '-')}`
      );
    }
    
    return this;
  }

  /**
   * 全体的な検証を実行
   */
  async verifyAll() {
    await this.navigateToWorkflowManager();
    await this.testWorkflowDetails();
    await this.verifySummaryButton();
    await this.verifyPipelineButton();
    
    return this;
  }
}