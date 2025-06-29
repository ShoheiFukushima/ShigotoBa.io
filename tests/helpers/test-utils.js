/**
 * E2Eテスト共通ユーティリティ関数
 */

import { expect } from '@playwright/test';
import { selectors, timeouts } from './common-selectors.js';

/**
 * ページの初期設定と待機
 */
export async function setupPage(page, url = '/') {
  await page.goto(url);
  await page.waitForLoadState('networkidle');
  await page.waitForSelector(selectors.header.title, { timeout: timeouts.pageLoad });
  await page.waitForTimeout(timeouts.long);
  return page;
}

/**
 * サイドバーの存在確認
 */
export async function verifySidebar(page) {
  const sidebar = page.locator(selectors.streamlit.sidebar);
  await expect(sidebar).toBeVisible();
  return sidebar;
}

/**
 * メトリクスの検証
 */
export async function verifyMetrics(page, expectedMetrics) {
  for (const metric of expectedMetrics) {
    const metricElement = page.locator(`text=${metric}`).first();
    await expect(metricElement).toBeVisible();
  }
}

/**
 * ボタンのクリックと待機
 */
export async function clickAndWait(element, waitTime = timeouts.medium) {
  await element.click();
  await element.page().waitForTimeout(waitTime);
}

/**
 * スクリーンショットの撮影
 */
export async function takeScreenshot(page, name, options = {}) {
  const defaultOptions = {
    path: `screenshots/${name}.png`,
    fullPage: true,
    ...options
  };
  
  await page.screenshot(defaultOptions);
}

/**
 * ビューポート変更とスクリーンショット
 */
export async function testResponsive(page, viewport, screenshotName) {
  await page.setViewportSize(viewport);
  await page.waitForTimeout(timeouts.medium);
  
  if (screenshotName) {
    await takeScreenshot(page, screenshotName);
  }
}

/**
 * 要素の存在を条件付きで確認
 */
export async function checkElementIfVisible(page, selector, assertion) {
  const element = typeof selector === 'string'
    ? page.locator(selector)
    : selector;
    
  const isVisible = await element.isVisible().catch(() => false);
  
  if (isVisible && assertion) {
    await assertion(element);
  }
  
  return isVisible;
}

/**
 * テキストを含む要素の取得
 */
export function getElementByText(page, text, elementType = '') {
  const selector = elementType 
    ? `${elementType}:has-text("${text}")`
    : `text=${text}`;
  
  return page.locator(selector);
}

/**
 * 複数の要素の可視性を一括確認
 */
export async function verifyElementsVisible(page, elements) {
  const results = {};
  
  for (const [key, selector] of Object.entries(elements)) {
    const element = page.locator(selector);
    const isVisible = await element.isVisible().catch(() => false);
    results[key] = isVisible;
    
    if (isVisible) {
      await expect(element).toBeVisible();
    }
  }
  
  return results;
}

/**
 * ページ遷移の待機とタイトル確認
 */
export async function waitForNavigation(page, expectedTitlePattern) {
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(timeouts.long);
  
  if (expectedTitlePattern) {
    const title = await page.title();
    expect(title).toMatch(expectedTitlePattern);
  }
}

/**
 * セレクトボックスの操作
 */
export async function selectOption(page, selectboxSelector, optionText) {
  const selectbox = page.locator(selectboxSelector);
  await selectbox.click();
  await page.waitForTimeout(timeouts.short);
  
  const option = page.locator(selectors.streamlit.selectboxOption)
    .filter({ hasText: optionText });
  
  if (await option.isVisible()) {
    await option.click();
    await page.waitForTimeout(timeouts.medium);
    return true;
  }
  
  return false;
}