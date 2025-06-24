#!/usr/bin/env python3
"""
運営分析ツール一覧ページ
データ分析・パフォーマンス監視・インサイト発見に関連するツールを整理して表示
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="運営分析ツール一覧 - shigotoba.io",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS（dev_tools_list.pyと同じスタイル）
st.markdown("""
<style>
    .tool-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid rgba(16, 185, 129, 0.2);
        transition: all 0.3s;
        height: 100%;
    }
    
    .tool-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
        border-color: rgba(16, 185, 129, 0.4);
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
        color: #10b981;
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
        background: linear-gradient(90deg, #10b981, #059669);
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
        color: #d1fae5;
        font-size: 1rem;
        margin: 5px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("# 📊 運営分析ツール一覧")
st.markdown("データ分析・パフォーマンス監視・戦略策定に必要なツールを整理して表示します")

# サイドバー
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from components.sidebar import render_sidebar
    render_sidebar()
except ImportError:
    pass

# ホームに戻るボタン
if st.button("🏠 ホームに戻る", type="secondary"):
    st.switch_page("app.py")

st.markdown("---")

# カテゴリ1: パフォーマンス監視・分析
st.markdown("""
<div class="category-header">
    <h2 class="category-title">📈 パフォーマンス監視・分析</h2>
    <p class="category-subtitle">リアルタイムでビジネス状況を把握・最適化</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">📈</span>
            <h3 class="tool-title">パフォーマンスダッシュボード</h3>
        </div>
        <div class="tool-description">
            ビジネス全体のKPIをリアルタイムで監視。売上・トラフィック・コンバージョンを統合的に分析。
        </div>
        <div class="tool-features">
            ✅ リアルタイム監視<br>
            ✅ KPI分析<br>
            ✅ トレンド予測<br>
            ✅ アラート機能
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📈 パフォーマンスダッシュボードを開く", key="performance", use_container_width=True):
        st.switch_page("pages/performance_dashboard.py")

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">🎯</span>
            <h3 class="tool-title">アトリビューション分析</h3>
        </div>
        <div class="tool-description">
            各マーケティングチャネルの貢献度を正確に測定。ROI最適化のための詳細な成果分析。
        </div>
        <div class="tool-features">
            ✅ チャネル分析<br>
            ✅ ROI測定<br>
            ✅ コンバージョン経路<br>
            ✅ 予算配分最適化
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 アトリビューション分析を開く", key="attribution", use_container_width=True):
        st.switch_page("pages/attribution_analysis.py")

# カテゴリ2: 顧客・ユーザー分析
st.markdown("""
<div class="category-header">
    <h2 class="category-title">👥 顧客・ユーザー分析</h2>
    <p class="category-subtitle">顧客理解を深め、体験価値を向上</p>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">🛤️</span>
            <h3 class="tool-title">カスタマージャーニーエンジン</h3>
        </div>
        <div class="tool-description">
            顧客の行動パターンを詳細に分析。タッチポイント最適化で顧客体験を向上させる高度なエンジン。
        </div>
        <div class="tool-features">
            ✅ 行動分析<br>
            ✅ ジャーニーマップ<br>
            ✅ タッチポイント最適化<br>
            ✅ 離脱防止策
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🛤️ カスタマージャーニーエンジンを開く", key="customer_journey", use_container_width=True):
        st.switch_page("pages/customer_journey_engine.py")

with col4:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">📊</span>
            <h3 class="tool-title">プロダクト分析</h3>
        </div>
        <div class="tool-description">
            プロダクトの利用状況を詳細に分析。機能別使用率・ユーザーセグメント・改善優先度を特定。
        </div>
        <div class="tool-features">
            ✅ 機能利用分析<br>
            ✅ ユーザーセグメント<br>
            ✅ 満足度調査<br>
            ✅ 改善提案
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 プロダクト分析を開く", key="product_analysis", use_container_width=True):
        st.switch_page("pages/product_analysis.py")

# カテゴリ3: AI・自動化分析
st.markdown("""
<div class="category-header">
    <h2 class="category-title">🤖 AI・自動化分析</h2>
    <p class="category-subtitle">AIを活用した高度な分析と予測</p>
</div>
""", unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">💬</span>
            <h3 class="tool-title">リアルタイムAIチャット</h3>
        </div>
        <div class="tool-description">
            データについて自然言語で質問可能。AI が即座に分析結果を返答し、インサイト発見を加速。
        </div>
        <div class="tool-features">
            ✅ 自然言語クエリ<br>
            ✅ 即座の回答<br>
            ✅ グラフ生成<br>
            ✅ 仮説検証
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💬 リアルタイムAIチャットを開く", key="ai_chat", use_container_width=True):
        st.switch_page("pages/realtime_chat.py")

with col6:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">⚙️</span>
            <h3 class="tool-title">AI設定</h3>
        </div>
        <div class="tool-description">
            AI分析エンジンの設定とカスタマイズ。モデル選択・パラメータ調整で最適な分析環境を構築。
        </div>
        <div class="tool-features">
            ✅ モデル選択<br>
            ✅ パラメータ調整<br>
            ✅ 学習データ管理<br>
            ✅ 精度監視
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚙️ AI設定を開く", key="ai_settings", use_container_width=True):
        st.switch_page("pages/ai_settings.py")

# 分析のベストプラクティス
st.markdown("---")
st.markdown("### 💡 分析のベストプラクティス")

practice_cols = st.columns(3)

with practice_cols[0]:
    st.info("""
    **📊 データドリブン経営**
    
    1. KPI設定の明確化
    2. 定期的な測定と改善
    3. 仮説検証サイクル
    """)

with practice_cols[1]:
    st.info("""
    **🎯 ROI最適化**
    
    1. アトリビューション分析
    2. チャネル効果測定
    3. 予算配分の最適化
    """)

with practice_cols[2]:
    st.info("""
    **👥 顧客中心分析**
    
    1. ジャーニー可視化
    2. セグメント別分析
    3. 体験価値向上
    """)

# 分析レポート機能
st.markdown("---")
st.markdown("### 📋 定期レポート機能")

report_cols = st.columns(2)

with report_cols[0]:
    st.markdown("""
    **🗓️ 自動レポート生成**
    - 週次パフォーマンスレポート
    - 月次分析サマリー
    - 四半期成長レポート
    """)

with report_cols[1]:
    st.markdown("""
    **📧 アラート通知**
    - KPI異常値検知
    - トレンド変化通知
    - 目標達成アラート
    """)

# フッター
st.markdown("---")
st.markdown("**🔗 関連ツール**: [新規開発ツール](dev_tools_list) | [広告マーケティングツール](marketing_tools_list)")