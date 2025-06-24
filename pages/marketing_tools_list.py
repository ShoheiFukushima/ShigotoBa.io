#!/usr/bin/env python3
"""
広告マーケティングツール一覧ページ
広告運用・コンテンツ制作・マーケティング実行に関連するツールを整理して表示
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="広告マーケティングツール一覧 - shigotoba.io",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .tool-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid rgba(245, 158, 11, 0.2);
        transition: all 0.3s;
        height: 100%;
    }
    
    .tool-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.2);
        border-color: rgba(245, 158, 11, 0.4);
    }
    
    .tool-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .tool-icon {
        font-size: 2rem;
        margin-right: 15px;
    }
    
    .tool-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #f59e0b;
        margin: 0;
    }
    
    .tool-description {
        color: #e2e8f0;
        margin-bottom: 15px;
        line-height: 1.6;
    }
    
    .tool-features {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    
    .category-header {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        padding: 20px;
        border-radius: 10px;
        margin: 30px 0 20px 0;
        text-align: center;
    }
    
    .category-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .category-subtitle {
        color: #fef3c7;
        font-size: 1rem;
        margin: 5px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("# 🎨 広告マーケティングツール一覧")
st.markdown("コンテンツ制作・広告運用・マーケティング実行に必要なツールを整理して表示します")

# ホームに戻るボタン
if st.button("🏠 ホームに戻る", type="secondary"):
    st.switch_page("app.py")

st.markdown("---")

# カテゴリ1: コンテンツ制作・AI活用
st.markdown("""
<div class="category-header">
    <h2 class="category-title">✨ コンテンツ制作・AI活用</h2>
    <p class="category-subtitle">AIを活用したクリエイティブ制作と最適化</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">🎨</span>
            <h3 class="tool-title">AI Creative Studio</h3>
        </div>
        <div class="tool-description">
            AIを活用したクリエイティブ制作の総合スタジオ。テキスト・画像・動画を統合的に生成・編集。
        </div>
        <div class="tool-features">
            ✅ AI文章生成<br>
            ✅ 画像生成・編集<br>
            ✅ 動画制作<br>
            ✅ ブランド統一
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎨 AI Creative Studioを開く", key="ai_creative", use_container_width=True):
        st.switch_page("pages/ai_creative_studio.py")

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">⚡</span>
            <h3 class="tool-title">リアルタイム広告最適化</h3>
        </div>
        <div class="tool-description">
            リアルタイムでの広告パフォーマンス監視と自動最適化。ROI最大化のための動的調整機能。
        </div>
        <div class="tool-features">
            ✅ リアルタイム監視<br>
            ✅ 自動入札調整<br>
            ✅ クリエイティブ切り替え<br>
            ✅ 予算配分最適化
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚡ リアルタイム広告最適化を開く", key="realtime_ad", use_container_width=True):
        st.switch_page("pages/realtime_ad_optimizer.py")

# カテゴリ2: マルチプラットフォーム運用
st.markdown("""
<div class="category-header">
    <h2 class="category-title">🌐 マルチプラットフォーム運用</h2>
    <p class="category-subtitle">複数チャネルを統合管理・効率的な運用</p>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">🌐</span>
            <h3 class="tool-title">マルチプラットフォーム管理</h3>
        </div>
        <div class="tool-description">
            複数のマーケティングチャネルを統合管理。SNS・広告・メールマーケティングを一元化。
        </div>
        <div class="tool-features">
            ✅ 統合ダッシュボード<br>
            ✅ 自動投稿<br>
            ✅ スケジュール管理<br>
            ✅ 効果測定
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌐 マルチプラットフォーム管理を開く", key="multi_platform", use_container_width=True):
        st.switch_page("pages/multi_platform_manager.py")

with col4:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">📅</span>
            <h3 class="tool-title">スケジューラー制御</h3>
        </div>
        <div class="tool-description">
            マーケティング活動のスケジュール管理と自動実行。キャンペーンタイミングを最適化。
        </div>
        <div class="tool-features">
            ✅ 投稿スケジュール<br>
            ✅ キャンペーン管理<br>
            ✅ 自動実行<br>
            ✅ 時間最適化
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📅 スケジューラー制御を開く", key="scheduler", use_container_width=True):
        st.switch_page("pages/scheduler_control.py")

# カテゴリ3: ビジネス戦略・価格設定
st.markdown("""
<div class="category-header">
    <h2 class="category-title">💰 ビジネス戦略・価格設定</h2>
    <p class="category-subtitle">科学的価格戦略とビジネス成長計画</p>
</div>
""", unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">💰</span>
            <h3 class="tool-title">価格戦略コンサルティング</h3>
        </div>
        <div class="tool-description">
            PSM分析・LTV/CAC計算・価格シミュレーションを含む包括的な価格戦略ツール。SaaSビジネスの最適価格を科学的に決定。
        </div>
        <div class="tool-features">
            ✅ PSM分析ツール<br>
            ✅ LTV/CAC計算機<br>
            ✅ 価格シミュレーター<br>
            ✅ 成長戦略ガイド
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💰 価格戦略コンサルティングを開く", key="pricing_strategy", use_container_width=True):
        st.switch_page("pages/pricing_strategy.py")

with col6:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">📊</span>
            <h3 class="tool-title">ビジネスモデル設計</h3>
        </div>
        <div class="tool-description">
            収益モデル・マネタイゼーション戦略の設計。サブスクリプション、フリーミアム、マーケットプレイスなど。
        </div>
        <div class="tool-features">
            ✅ 収益モデル設計<br>
            ✅ マネタイゼーション最適化<br>
            ✅ ユニットエコノミクス<br>
            ✅ 成長戦略立案
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 ビジネスモデル設計を開く", key="business_model", use_container_width=True):
        st.switch_page("pages/business_model_design.py")

# カテゴリ4: 自動化・実行管理
st.markdown("""
<div class="category-header">
    <h2 class="category-title">🤖 自動化・実行管理</h2>
    <p class="category-subtitle">マーケティング活動の自動化と効率化</p>
</div>
""", unsafe_allow_html=True)

col7, col8 = st.columns(2)

with col7:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">🚀</span>
            <h3 class="tool-title">自動投稿</h3>
        </div>
        <div class="tool-description">
            コンテンツの自動投稿・配信システム。最適なタイミングでのマルチチャネル配信を実現。
        </div>
        <div class="tool-features">
            ✅ 自動投稿<br>
            ✅ 最適タイミング<br>
            ✅ マルチチャネル<br>
            ✅ 効果追跡
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 自動投稿を開く", key="auto_posting", use_container_width=True):
        st.switch_page("pages/auto_posting.py")

with col8:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">📚</span>
            <h3 class="tool-title">マニュアル</h3>
        </div>
        <div class="tool-description">
            マーケティングツールの使い方・ベストプラクティス・トラブルシューティングガイド。
        </div>
        <div class="tool-features">
            ✅ 使い方ガイド<br>
            ✅ ベストプラクティス<br>
            ✅ トラブルシューティング<br>
            ✅ 更新情報
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📚 マニュアルを開く", key="user_manual", use_container_width=True):
        st.switch_page("pages/user_manual.py")

# マーケティング戦略ガイド
st.markdown("---")
st.markdown("### 💡 マーケティング戦略ガイド")

strategy_cols = st.columns(3)

with strategy_cols[0]:
    st.info("""
    **🎯 コンテンツマーケティング**
    
    1. AI Creative Studioで制作
    2. マルチプラットフォームで配信
    3. パフォーマンス分析
    """)

with strategy_cols[1]:
    st.info("""
    **📊 データドリブン運用**
    
    1. リアルタイム最適化
    2. A/Bテストで検証
    3. 自動化で効率化
    """)

with strategy_cols[2]:
    st.info("""
    **🚀 スケールアップ**
    
    1. 自動投稿で効率化
    2. 統合管理で品質維持
    3. 継続的な改善
    """)

# キャンペーン成功事例
st.markdown("---")
st.markdown("### 🏆 キャンペーン成功事例")

case_cols = st.columns(2)

with case_cols[0]:
    st.markdown("""
    **📈 EC売上300%向上事例**
    - AI Creative Studioでクリエイティブ制作
    - リアルタイム最適化で効果最大化
    - 結果: CVR 2.3% → 6.9%
    """)

with case_cols[1]:
    st.markdown("""
    **🌟 ブランド認知度向上事例**
    - マルチプラットフォーム統合運用
    - 自動投稿でコンスタント配信
    - 結果: エンゲージメント250%向上
    """)

# ROI計算ツール
st.markdown("---")
st.markdown("### 💰 ROI計算・予算管理")

roi_cols = st.columns(2)

with roi_cols[0]:
    st.markdown("""
    **📊 ROI追跡指標**
    - 広告費用対効果 (ROAS)
    - 顧客獲得コスト (CAC)
    - 顧客生涯価値 (LTV)
    """)

with roi_cols[1]:
    st.markdown("""
    **🎯 予算最適化**
    - チャネル別予算配分
    - 自動入札調整
    - リアルタイム予算管理
    """)

# フッター
st.markdown("---")
st.markdown("**🔗 関連ツール**: [新規開発ツール](dev_tools_list) | [運営分析ツール](analysis_tools_list)")