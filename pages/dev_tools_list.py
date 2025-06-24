#!/usr/bin/env python3
"""
新規開発ツール一覧ページ
プロジェクト開発に関連するツールを整理して表示
"""

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="新規開発ツール一覧 - shigotoba.io",
    page_icon="🏗️",
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
        border: 1px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s;
        height: 100%;
    }
    
    .tool-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.4);
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
        color: #3b82f6;
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
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
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
        color: #dbeafe;
        font-size: 1rem;
        margin: 5px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("# 🏗️ 新規開発ツール一覧")
st.markdown("プロジェクト開発・管理に必要なツールを整理して表示します")

# ホームに戻るボタン
if st.button("🏠 ホームに戻る", type="secondary"):
    st.switch_page("app.py")

st.markdown("---")

# カテゴリ1: プロジェクト管理・企画
st.markdown("""
<div class="category-header">
    <h2 class="category-title">📋 プロジェクト管理・企画</h2>
    <p class="category-subtitle">アイデア創出から完成まで、プロジェクト全体を管理</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">🏗️</span>
            <h3 class="tool-title">開発室</h3>
        </div>
        <div class="tool-description">
            新しいプロジェクトの企画・設計・開発を行うメインツール。アイデアから実装まで一貫してサポート。
        </div>
        <div class="tool-features">
            ✅ プロジェクト作成<br>
            ✅ 要件定義<br>
            ✅ 技術選択<br>
            ✅ 開発計画
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏗️ 開発室を開く", key="dev_room", use_container_width=True):
        st.switch_page("pages/development_room.py")

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">📊</span>
            <h3 class="tool-title">プロジェクト管理室</h3>
        </div>
        <div class="tool-description">
            進行中のプロジェクトを効率的に管理。スケジュール・リソース・品質を総合的に監視。
        </div>
        <div class="tool-features">
            ✅ 進捗管理<br>
            ✅ タスク分析<br>
            ✅ チーム協業<br>
            ✅ 品質管理
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 プロジェクト管理室を開く", key="project_mgmt", use_container_width=True):
        st.switch_page("pages/project_management.py")

# カテゴリ2: プロダクト開発・テスト
st.markdown("""
<div class="category-header">
    <h2 class="category-title">🎯 プロダクト開発・テスト</h2>
    <p class="category-subtitle">製品の品質向上と最適化を実現</p>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">📦</span>
            <h3 class="tool-title">プロダクト管理</h3>
        </div>
        <div class="tool-description">
            プロダクトのライフサイクル全体を管理。機能追加から改善まで、製品価値を最大化。
        </div>
        <div class="tool-features">
            ✅ 機能管理<br>
            ✅ バージョン管理<br>
            ✅ ユーザーフィードバック<br>
            ✅ 改善計画
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📦 プロダクト管理を開く", key="product_mgmt", use_container_width=True):
        st.switch_page("pages/product_management.py")

with col4:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <span class="tool-icon">🧪</span>
            <h3 class="tool-title">A/Bテスト</h3>
        </div>
        <div class="tool-description">
            データドリブンな意思決定をサポート。複数の案を科学的に比較検証して最適解を発見。
        </div>
        <div class="tool-features">
            ✅ 実験設計<br>
            ✅ 統計分析<br>
            ✅ 結果可視化<br>
            ✅ 意思決定支援
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🧪 A/Bテストを開く", key="ab_testing", use_container_width=True):
        st.switch_page("pages/ab_testing.py")

# 開発チーム向け情報
st.markdown("---")
st.markdown("### 💡 開発のヒント")

info_cols = st.columns(3)

with info_cols[0]:
    st.info("""
    **🚀 スタートアップ向け**
    
    1. 開発室でMVP企画
    2. A/Bテストで検証
    3. プロダクト管理で改善
    """)

with info_cols[1]:
    st.info("""
    **🏢 企業向け**
    
    1. プロジェクト管理室で統制
    2. 開発室で新機能開発
    3. 継続的な品質管理
    """)

with info_cols[2]:
    st.info("""
    **👥 チーム開発**
    
    1. 役割分担の明確化
    2. 進捗の透明性確保
    3. 品質基準の統一
    """)

# フッター
st.markdown("---")
st.markdown("**🔗 関連ツール**: [運営分析ツール](analysis_tools_list) | [広告マーケティングツール](marketing_tools_list)")