/**
 * 共通セレクター定義
 * E2Eテスト全体で使用するセレクターを一元管理
 */

export const selectors = {
  // Streamlit基本要素
  streamlit: {
    sidebar: '[data-testid="stSidebar"]',
    main: 'section[data-testid="stMain"]',
    selectbox: '[data-testid="stSelectbox"]',
    selectboxOption: '[data-testid="stSelectboxOption"]',
    button: '[data-testid="stButton"]',
    metric: '[data-testid="metric-container"]',
    metricLabel: '[data-testid="stMetricLabel"]',
    metricValue: '[data-testid="stMetricValue"]',
    alert: '[role="alert"]',
    hamburger: '[data-testid="stSidebarCollapsedControl"]'
  },

  // ヘッダー要素
  header: {
    title: 'h1',
    subtitle: 'h2',
    sectionTitle: 'h3'
  },

  // サイドバー要素
  sidebar: {
    branding: 'text=SHIGOTOBA.IO',
    menuButton: (text) => `button:has-text("${text}")`,
    statistics: {
      task: 'text=タスク',
      post: 'text=投稿',
      content: 'text=コンテンツ',
      efficiency: 'text=効果'
    },
    footer: 'text=© 2024'
  },

  // ダッシュボード要素
  dashboard: {
    title: 'h1:has-text("ダッシュボード")',
    googleSheetsStatus: '[role="alert"]:has-text("Google Sheets")',
    metricsSection: 'h2:has-text("今日の概要")',
    projectSection: 'h2:has-text("プロジェクト一覧")',
    quickAccessSection: 'h2:has-text("クイックアクセス")',
    welcomeMessage: 'text=shigotoba.io へようこそ',
    tourButton: 'button:has-text("ツアーを開始")'
  },

  // ワークフロー管理要素
  workflow: {
    managerButton: 'button:has-text("ワークフロー管理")',
    detailButton: 'button:has-text("詳細を見る")',
    actionButtons: 'button:has-text(/実行|編集|削除|一時停止/)',
    stepSection: 'text=ステップ'
  },

  // カテゴリセクション
  categories: {
    development: 'h3:has-text("🏗️ 新規開発")',
    analytics: 'h3:has-text("📊 運営・分析")',
    marketing: 'h3:has-text("🎨 広告・マーケティング実行")',
    automation: 'h3:has-text("🔄 自動化パイプライン")'
  }
};

/**
 * 待機時間の定数
 */
export const timeouts = {
  short: 300,
  medium: 500,
  long: 2000,
  pageLoad: 30000
};

/**
 * ビューポートサイズ
 */
export const viewports = {
  desktop: { width: 1920, height: 1080 },
  tablet: { width: 768, height: 1024 },
  mobile: { width: 375, height: 667 }
};