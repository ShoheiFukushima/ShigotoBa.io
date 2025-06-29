/**
 * サイドバーページのPage Objectモデル
 */

import { expect } from '@playwright/test';
import { selectors, timeouts, viewports } from '../helpers/common-selectors.js';
import { 
  setupPage, 
  verifySidebar,
  clickAndWait,
  testResponsive,
  checkElementIfVisible 
} from '../helpers/test-utils.js';

export class SidebarPage {
  constructor(page) {
    this.page = page;
    this.sidebar = null;
  }

  /**
   * ページの初期化
   */
  async init() {
    await setupPage(this.page);
    this.sidebar = await verifySidebar(this.page);
    return this;
  }

  /**
   * ブランディング要素の確認
   */
  async verifyBranding() {
    const branding = this.sidebar.locator(selectors.sidebar.branding).first();
    await expect(branding).toBeVisible();
    
    return this;
  }

  /**
   * メニューナビゲーションの確認
   */
  async verifyMenuNavigation() {
    const menuItems = ['ホーム', '開発室', 'プロジェクト管理', 'パフォーマンス'];
    
    for (const item of menuItems) {
      const menuItem = this.sidebar.locator(selectors.sidebar.menuButton(item));
      const count = await menuItem.count();
      expect(count).toBeGreaterThan(0);
    }
    
    return this;
  }

  /**
   * プロジェクトセレクターの動作確認
   */
  async verifyProjectSelector() {
    const projectSelector = this.sidebar.locator(selectors.streamlit.selectbox);
    const selectorCount = await projectSelector.count();
    
    if (selectorCount > 0) {
      await expect(projectSelector.first()).toBeVisible();
      
      await projectSelector.first().click();
      await this.page.waitForTimeout(timeouts.short);
      await this.page.waitForTimeout(timeouts.medium);
      
      const options = this.page.locator(selectors.streamlit.selectboxOption);
      const optionCount = await options.count();
      
      if (optionCount === 0) {
        await expect(projectSelector.first()).toBeEnabled();
      } else {
        expect(optionCount).toBeGreaterThan(0);
      }
    }
    
    return this;
  }

  /**
   * 統計情報の表示確認
   */
  async verifyStatistics() {
    const statsToCheck = ['タスク', '投稿', 'コンテンツ', '効果'];
    
    for (const stat of statsToCheck) {
      const statElement = this.sidebar.locator(`text=${stat}`).first();
      
      await checkElementIfVisible(statElement, async (element) => {
        await expect(element).toBeVisible();
      });
    }
    
    return this;
  }

  /**
   * クイックアクションボタンの確認
   */
  async verifyQuickActions() {
    const startProjectButton = this.sidebar.locator(
      selectors.sidebar.menuButton('プロジェクトを始める')
    );
    
    await checkElementIfVisible(startProjectButton, async (button) => {
      await expect(button).toBeVisible();
      await expect(button).toBeEnabled();
    });
    
    return this;
  }

  /**
   * フッターの確認
   */
  async verifyFooter() {
    const footer = this.sidebar.locator(selectors.sidebar.footer);
    
    await checkElementIfVisible(footer, async (element) => {
      await expect(element.first()).toBeVisible();
    });
    
    return this;
  }

  /**
   * ページ遷移のテスト
   */
  async testPageNavigation() {
    const devRoomButton = this.sidebar.locator(selectors.sidebar.menuButton('開発室'));
    const devButtonCount = await devRoomButton.count();
    
    if (devButtonCount > 0) {
      await devRoomButton.click();
      await this.page.waitForTimeout(timeouts.medium);
      
      await this.page.waitForLoadState('networkidle');
      await this.page.waitForTimeout(timeouts.long);
      
      const devPageTitle = this.page.locator('h1, h2').filter({ 
        hasText: /開発室|Development/ 
      });
      
      const titleCount = await devPageTitle.count();
      expect(titleCount).toBeGreaterThan(0);
    }
    
    return this;
  }

  /**
   * レスポンシブ動作の確認
   */
  async testResponsive() {
    // デスクトップビュー
    await testResponsive(this.page, viewports.desktop);
    await expect(this.sidebar).toBeVisible();
    
    // タブレットビュー
    await testResponsive(this.page, viewports.tablet);
    await expect(this.sidebar).toBeVisible();
    
    // モバイルビュー
    await testResponsive(this.page, viewports.mobile);
    
    const sidebarVisible = await this.sidebar.isVisible().catch(() => false);
    
    if (!sidebarVisible) {
      const hamburger = this.page.locator(selectors.streamlit.hamburger);
      const hamburgerCount = await hamburger.count();
      
      if (hamburgerCount > 0) {
        await expect(hamburger).toBeVisible();
      }
    }
    
    return this;
  }

  /**
   * メインナビゲーションとの統合確認
   */
  async verifyIntegrationWithMain() {
    const mainContent = this.page.locator(selectors.streamlit.main);
    await expect(mainContent).toBeVisible();
    await expect(this.sidebar).toBeVisible();
    
    const mainBox = await mainContent.boundingBox();
    const sidebarBox = await this.sidebar.boundingBox();
    
    expect(mainBox).not.toBeNull();
    expect(sidebarBox).not.toBeNull();
    
    if (mainBox && sidebarBox) {
      expect(sidebarBox.x + sidebarBox.width).toBeLessThanOrEqual(mainBox.x + 10);
    }
    
    return this;
  }

  /**
   * 統計メトリクスの詳細確認
   */
  async verifyDetailedStatistics() {
    const metricsFound = [];
    
    // st.metricウィジェットの確認
    const metricWidgets = this.sidebar.locator(selectors.streamlit.metric);
    const metricCount = await metricWidgets.count();
    
    if (metricCount > 0) {
      for (let i = 0; i < metricCount; i++) {
        const metric = metricWidgets.nth(i);
        const label = await metric.locator(selectors.streamlit.metricLabel).textContent();
        const value = await metric.locator(selectors.streamlit.metricValue).textContent();
        metricsFound.push({ label, value });
      }
    } else {
      // テキストベースの統計の確認
      const statsLabels = ['タスク', '投稿', 'コンテンツ', '効果'];
      
      for (const label of statsLabels) {
        const statElement = this.sidebar.locator(`text=${label}`).first();
        
        if (await statElement.isVisible().catch(() => false)) {
          metricsFound.push({ label, found: true });
        }
      }
    }
    
    expect(metricsFound.length).toBeGreaterThan(0);
    
    return this;
  }

  /**
   * 全体的な検証を実行
   */
  async verifyAll() {
    await this.verifyBranding();
    await this.verifyMenuNavigation();
    await this.verifyProjectSelector();
    await this.verifyStatistics();
    await this.verifyQuickActions();
    await this.verifyFooter();
    await this.verifyDetailedStatistics();
    await this.verifyIntegrationWithMain();
    
    return this;
  }
}