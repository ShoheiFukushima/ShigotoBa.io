#!/usr/bin/env python3
"""
システムマニュアル - マーケティング自動化ダッシュボードの使い方
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="システムマニュアル",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    /* ダークモード設定 */
    .stApp {
        background-color: #0e1117;
    }
    
    /* マニュアルヘッダー */
    .manual-header {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .manual-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: manualPulse 8s ease-in-out infinite;
    }
    
    @keyframes manualPulse {
        0%, 100% { transform: scale(0.8) rotate(0deg); opacity: 0.3; }
        50% { transform: scale(1.2) rotate(180deg); opacity: 0.6; }
    }
    
    .manual-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .manual-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* セクションカード */
    .section-card {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 2px solid rgba(16, 185, 129, 0.3);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .section-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.2);
        border-color: #10b981;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #10b981;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    
    .section-icon {
        margin-right: 10px;
        font-size: 1.8rem;
    }
    
    /* ステップガイド */
    .step-guide {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin: 15px 0;
    }
    
    .step-number {
        background: #10b981;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 15px;
    }
    
    /* 機能説明 */
    .feature-box {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .feature-title {
        color: #3b82f6;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* 注意事項 */
    .note-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .warning-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class="manual-header">
    <div class="manual-title">📚 システムマニュアル</div>
    <div class="manual-subtitle">マーケティング自動化ダッシュボード完全ガイド</div>
</div>
""", unsafe_allow_html=True)

# 目次
st.markdown("## 📋 目次")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    1. **システム概要**
    2. **基本操作**
    3. **プロジェクト開発機能**
    4. **運営・分析機能**
    """)

with col2:
    st.markdown("""
    5. **広告・マーケティング機能**
    6. **AI機能の活用**
    7. **トラブルシューティング**
    8. **よくある質問**
    """)

st.markdown("---")

# 1. システム概要
st.markdown("""
<div class="section-card">
    <div class="section-title">
        <span class="section-icon">🎯</span>
        1. システム概要
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
このシステムは、**マーケティング業務を自動化・効率化**するための統合ダッシュボードです。

### 🚀 主な特徴：
- **AI駆動の自動化**: Gemini APIを活用した高度な分析・生成機能
- **統合管理**: 複数のマーケティングツールを一元管理
- **リアルタイム最適化**: データに基づく自動最適化
- **カスタマイズ可能**: あなたの業務に合わせて設定調整

### 🏗️ システム構成：
""")

st.markdown("""
<div class="feature-box">
    <div class="feature-title">🏗️ プロジェクト開発</div>
    新規プロジェクトの企画・開発・管理を行う機能群
</div>

<div class="feature-box">
    <div class="feature-title">📈 プロジェクト運営・分析</div>
    既存プロジェクトの分析・最適化・レポート生成機能
</div>

<div class="feature-box">
    <div class="feature-title">🎨 広告・マーケティング実行</div>
    AI駆動の広告作成・配信・最適化機能
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 2. 基本操作
st.markdown("""
<div class="section-card">
    <div class="section-title">
        <span class="section-icon">🖱️</span>
        2. 基本操作
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🏠 ホーム画面の使い方

<div class="step-guide">
    <span class="step-number">1</span>
    <strong>ダッシュボード確認</strong><br>
    アクティブプロジェクト数、未完了タスク、効率スコアなどの重要指標を確認
</div>

<div class="step-guide">
    <span class="step-number">2</span>
    <strong>クイックアクセス</strong><br>
    3つのカテゴリから目的の機能にワンクリックでアクセス
</div>

<div class="step-guide">
    <span class="step-number">3</span>
    <strong>ドキュメント書庫</strong><br>
    ツリー表示でマニュアル・レポート・素材を効率的に管理
</div>

### 🧭 ナビゲーション
- **パンくずリスト**: 現在の画面位置を確認
- **サイドバー**: クイックアクション、統計、通知を表示
- **戻るボタン**: 各ページから簡単にホームに戻る
""")

st.markdown("---")

# 3. プロジェクト開発機能
st.markdown("""
<div class="section-card">
    <div class="section-title">
        <span class="section-icon">🏗️</span>
        3. プロジェクト開発機能
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🏗️ 開発室
新しいマーケティングプロジェクトを0から企画・開発します。

<div class="feature-box">
    <div class="feature-title">プロジェクト作成フロー</div>
    1. プロジェクト名・説明の入力<br>
    2. ターゲット市場・顧客の設定<br>
    3. 予算・期間の設定<br>
    4. AIによる戦略提案<br>
    5. マーケティングプランの生成
</div>

### 📊 プロジェクト管理室
既存プロジェクトの進捗管理・チーム協働を支援します。

<div class="feature-box">
    <div class="feature-title">主要機能</div>
    • プロジェクト一覧・フィルタリング<br>
    • 進捗トラッキング<br>
    • チームメンバー管理<br>
    • マイルストーン設定<br>
    • 自動レポート生成
</div>

### 📦 プロダクト管理
製品・サービスの情報を一元管理します。

<div class="feature-box">
    <div class="feature-title">管理項目</div>
    • 製品基本情報<br>
    • 価格・料金体系<br>
    • 競合分析データ<br>
    • 市場ポジション<br>
    • バージョン履歴
</div>

### 🧪 A/Bテスト
科学的なマーケティング実験を実施します。

<div class="feature-box">
    <div class="feature-title">テスト機能</div>
    • 実験設計ウィザード<br>
    • 統計的有意性の自動計算<br>
    • サンプルサイズ計算<br>
    • 結果の自動分析<br>
    • レポート自動生成
</div>
""")

st.markdown("---")

# 4. 運営・分析機能
st.markdown("""
<div class="section-card">
    <div class="section-title">
        <span class="section-icon">📈</span>
        4. プロジェクト運営・分析機能
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 📈 パフォーマンスダッシュボード
マーケティング活動の成果を可視化・分析します。

<div class="feature-box">
    <div class="feature-title">主要KPI</div>
    • コンバージョン率<br>
    • 顧客獲得コスト (CAC)<br>
    • 顧客生涯価値 (LTV)<br>
    • ROI・ROAS<br>
    • エンゲージメント率
</div>

### 🎯 アトリビューション分析
顧客の購買経路を詳細に分析します。

<div class="feature-box">
    <div class="feature-title">分析モデル</div>
    • First-Touch Attribution<br>
    • Last-Touch Attribution<br>
    • Linear Attribution<br>
    • Time-Decay Attribution<br>
    • U-Shaped Attribution<br>
    • カスタムMLモデル
</div>

### 🛤️ カスタマージャーニーエンジン
AI駆動の顧客行動予測・最適化を行います。

<div class="feature-box">
    <div class="feature-title">予測機能</div>
    • 顧客セグメンテーション<br>
    • チャーン予測<br>
    • 次回購入予測<br>
    • 最適なタッチポイント提案<br>
    • ジャーニー最適化
</div>

### 💬 AIチャット
リアルタイムでAIアシスタントと対話できます。

<div class="feature-box">
    <div class="feature-title">対話内容</div>
    • データ分析の質問<br>
    • 戦略相談<br>
    • レポート作成依頼<br>
    • 技術的なサポート<br>
    • アイデア出し
</div>
""")

st.markdown("---")

# 5. 広告・マーケティング機能
st.markdown("""
<div class="section-card">
    <div class="section-title">
        <span class="section-icon">🎨</span>
        5. 広告・マーケティング実行機能
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🎨 AI Creative Studio
AIを活用したクリエイティブコンテンツの自動生成を行います。

<div class="feature-box">
    <div class="feature-title">生成可能なコンテンツ</div>
    • 広告コピー（見出し・本文・CTA）<br>
    • SNSコンテンツ（投稿文・ハッシュタグ）<br>
    • 動画スクリプト（シナリオ・ナレーション）<br>
    • メールキャンペーン（件名・本文）<br>
    • ブログ記事（アウトライン・本文）
</div>

<div class="step-guide">
    <span class="step-number">1</span>
    <strong>クリエイティブタイプ選択</strong><br>
    作成したいコンテンツの種類を選択
</div>

<div class="step-guide">
    <span class="step-number">2</span>
    <strong>ターゲット・ブランド情報入力</strong><br>
    対象顧客とブランドの特徴を設定
</div>

<div class="step-guide">
    <span class="step-number">3</span>
    <strong>AI生成・パフォーマンス予測</strong><br>
    AIがコンテンツを生成し、効果を予測
</div>

### ⚡ リアルタイム広告最適化
機械学習による自動広告最適化エンジンです。

<div class="feature-box">
    <div class="feature-title">最適化項目</div>
    • 入札価格の自動調整<br>
    • ターゲット層の最適化<br>
    • 広告文・画像の自動テスト<br>
    • 配信時間の最適化<br>
    • 予算配分の自動調整
</div>

### 🌐 マルチプラットフォーム管理
複数の広告プラットフォームを統合管理します。

<div class="feature-box">
    <div class="feature-title">対応プラットフォーム</div>
    • Google Ads<br>
    • Facebook Ads<br>
    • Instagram Ads<br>
    • Twitter Ads<br>
    • LinkedIn Ads<br>
    • TikTok Ads
</div>

<div class="feature-box">
    <div class="feature-title">統合機能</div>
    • クロスプラットフォーム分析<br>
    • 予算の自動配分<br>
    • 統一されたレポート<br>
    • オーディエンス同期<br>
    • 一括キャンペーン管理
</div>
""")

st.markdown("---")

# 6. AI機能の活用
st.markdown("""
<div class="section-card">
    <div class="section-title">
        <span class="section-icon">🤖</span>
        6. AI機能の活用方法
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🧠 Gemini AI統合
システム全体でGoogle Gemini APIを活用しています。

<div class="feature-box">
    <div class="feature-title">AI活用シーン</div>
    • コンテンツ自動生成<br>
    • データ分析・洞察抽出<br>
    • 戦略提案・アドバイス<br>
    • 予測分析・レコメンド<br>
    • 自動レポート作成
</div>

### ⚙️ AI設定
AIモデルの設定・管理を行います。

<div class="step-guide">
    <span class="step-number">1</span>
    <strong>APIキー設定</strong><br>
    Gemini APIキーを設定（他のAIプロバイダーも今後追加予定）
</div>

<div class="step-guide">
    <span class="step-number">2</span>
    <strong>モデル選択</strong><br>
    タスクに応じて最適なAIモデルを選択
</div>

<div class="step-guide">
    <span class="step-number">3</span>
    <strong>パラメータ調整</strong><br>
    創造性やコスト効率を調整
</div>

<div class="note-box">
    💡 <strong>ヒント：</strong> AIチャット機能を使って、システムの使い方やマーケティング戦略について質問できます。
</div>
""")

st.markdown("---")

# 7. トラブルシューティング
st.markdown("""
<div class="section-card">
    <div class="section-title">
        <span class="section-icon">🔧</span>
        7. トラブルシューティング
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🚨 よくある問題と解決法

<div class="warning-box">
    <strong>⚠️ ページが表示されない</strong><br>
    • ブラウザのキャッシュをクリア<br>
    • 別のブラウザで試す<br>
    • サーバーの再起動（ターミナルでCtrl+Cして再実行）
</div>

<div class="warning-box">
    <strong>⚠️ AI機能が動作しない</strong><br>
    • AI設定ページでAPIキーを確認<br>
    • インターネット接続を確認<br>
    • APIの利用制限に達していないか確認
</div>

<div class="warning-box">
    <strong>⚠️ データが保存されない</strong><br>
    • セッションがタイムアウトしていないか確認<br>
    • ページをリロードして再試行<br>
    • ブラウザのJavaScriptが有効か確認
</div>

### 🔄 システム再起動方法

<div class="step-guide">
    <span class="step-number">1</span>
    <strong>ターミナルでCtrl+C</strong><br>
    実行中のStreamlitを停止
</div>

<div class="step-guide">
    <span class="step-number">2</span>
    <strong>再起動コマンド実行</strong><br>
    <code>cd dashboard && python3 -m streamlit run home.py</code>
</div>
""")

st.markdown("---")

# 8. よくある質問
st.markdown("""
<div class="section-card">
    <div class="section-title">
        <span class="section-icon">❓</span>
        8. よくある質問（FAQ）
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🤔 一般的な質問

**Q: このシステムは無料で使えますか？**
A: システム自体は無料ですが、AI機能（Gemini API）の利用には料金が発生する場合があります。

**Q: データはどこに保存されますか？**
A: 現在はブラウザのセッション内に保存されています。永続化が必要な場合はデータベース連携を追加できます。

**Q: 他のAIサービスも使えますか？**
A: 現在はGemini APIのみですが、OpenAI、Anthropic Claudeなどの追加予定があります。

**Q: スマートフォンでも使えますか？**
A: レスポンシブデザインに対応しているため、スマートフォンやタブレットでも利用可能です。

**Q: 複数人で同時に使えますか？**
A: 現在は個人利用向けです。チーム利用にはユーザー認証機能の追加が必要です。

### 🛠️ 技術的な質問

**Q: 新しい機能を追加できますか？**
A: はい、モジュール式の設計のため、新機能の追加が容易です。

**Q: データのエクスポートはできますか？**
A: 各ページで生成されたレポートやデータはCSV、PDF形式でエクスポート可能です。

**Q: API連携は可能ですか？**
A: 外部サービスとのAPI連携機能を追加できます。

<div class="note-box">
    💡 <strong>さらに詳しく知りたい場合：</strong><br>
    AIチャット機能で具体的な質問をするか、各機能ページのヘルプセクションをご確認ください。
</div>
""")

st.markdown("---")

# フッター
st.markdown("""
<div style="text-align: center; padding: 20px; color: #94a3b8;">
    <strong>マーケティング自動化ダッシュボード</strong><br>
    Version 1.0 | AI-Powered Marketing Automation System
</div>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("📚 マニュアル目次")
    
    if st.button("🎯 システム概要", use_container_width=True):
        st.markdown('<a href="#システム概要">システム概要へ</a>', unsafe_allow_html=True)
    
    if st.button("🖱️ 基本操作", use_container_width=True):
        st.markdown('<a href="#基本操作">基本操作へ</a>', unsafe_allow_html=True)
    
    if st.button("🏗️ プロジェクト開発", use_container_width=True):
        st.markdown('<a href="#プロジェクト開発機能">プロジェクト開発へ</a>', unsafe_allow_html=True)
    
    if st.button("📈 運営・分析", use_container_width=True):
        st.markdown('<a href="#プロジェクト運営・分析機能">運営・分析へ</a>', unsafe_allow_html=True)
    
    if st.button("🎨 広告・マーケティング", use_container_width=True):
        st.markdown('<a href="#広告・マーケティング実行機能">広告・マーケティングへ</a>', unsafe_allow_html=True)
    
    if st.button("🤖 AI機能", use_container_width=True):
        st.markdown('<a href="#AI機能の活用方法">AI機能へ</a>', unsafe_allow_html=True)
    
    if st.button("🔧 トラブルシューティング", use_container_width=True):
        st.markdown('<a href="#トラブルシューティング">トラブルシューティングへ</a>', unsafe_allow_html=True)
    
    if st.button("❓ よくある質問", use_container_width=True):
        st.markdown('<a href="#よくある質問（FAQ）">よくある質問へ</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("home.py")